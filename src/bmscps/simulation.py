"""End-to-end resilient battery-management cyber-physical simulation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .attacks import AttackConfig, apply_attack
from .battery import BatteryParams, initial_state, step_battery, terminal_voltage_v
from .controller import ControllerConfig, control
from .detector import DetectorConfig, ResidualDetector
from .network import NetworkChannel, NetworkConfig
from .twin import DigitalTwin, residuals


@dataclass(frozen=True)
class SimulationConfig:
    steps: int = 400
    dt_s: float = 1.0
    sensor_noise_std_v: float = 0.005
    sensor_noise_std_temp_c: float = 0.08
    sensor_noise_std_soc: float = 0.001
    random_seed: int = 11


def run_simulation(
    battery: BatteryParams | None = None,
    sim: SimulationConfig | None = None,
    network: NetworkConfig | None = None,
    attack: AttackConfig | None = None,
    detector: DetectorConfig | None = None,
    controller: ControllerConfig | None = None,
) -> dict[str, np.ndarray]:
    p = battery or BatteryParams()
    scfg = sim or SimulationConfig()
    ncfg = network or NetworkConfig()
    acfg = attack or AttackConfig()
    dcfg = detector or DetectorConfig()
    ccfg = controller or ControllerConfig()
    if scfg.steps <= 0 or scfg.dt_s <= 0:
        raise ValueError("steps and dt_s must be positive")

    rng = np.random.default_rng(scfg.random_seed)
    plant = initial_state(p)
    twin = DigitalTwin.create(p)
    channel = NetworkChannel(ncfg)
    detector_obj = ResidualDetector(dcfg)

    keys = [
        "time_s", "true_soc", "measured_soc", "twin_soc", "true_temperature_c",
        "measured_temperature_c", "twin_temperature_c", "true_voltage_v", "measured_voltage_v",
        "twin_voltage_v", "current_command_a", "cooling_power_w", "residual_voltage_v",
        "residual_temperature_c", "residual_soc", "anomaly_score", "anomaly", "controller_state",
        "packet_received"
    ]
    out = {k: np.zeros(scfg.steps, dtype=float) for k in keys}
    last_received: dict[str, float] | None = None
    replay_buffer: dict[str, float] | None = None
    current_cmd = ccfg.nominal_current_a
    cooling_cmd = 0.0

    for step in range(scfg.steps):
        plant = step_battery(p, plant, current_cmd, cooling_cmd, scfg.dt_s)
        true_v = terminal_voltage_v(p, plant, current_cmd)
        measured = {
            "soc": plant.soc + rng.normal(0.0, scfg.sensor_noise_std_soc),
            "temperature_c": plant.temperature_c + rng.normal(0.0, scfg.sensor_noise_std_temp_c),
            "voltage_v": true_v + rng.normal(0.0, scfg.sensor_noise_std_v),
        }
        if replay_buffer is None and step == max(0, acfg.start_step - 10):
            replay_buffer = dict(measured)
        packet = apply_attack(measured, step, acfg, replay_buffer)
        channel.send(step, packet)
        received = channel.receive(step)
        packet_received = received is not None
        if received is not None:
            last_received = received
        cyber_measurement = last_received or packet

        predicted = twin.predict(current_cmd, cooling_cmd, scfg.dt_s)
        r = residuals(cyber_measurement, predicted)
        anomaly, score = detector_obj.update(r)
        state_code, current_cmd, cooling_cmd = control(cyber_measurement["temperature_c"], anomaly, ccfg)

        out["time_s"][step] = step * scfg.dt_s
        out["true_soc"][step] = plant.soc
        out["measured_soc"][step] = cyber_measurement["soc"]
        out["twin_soc"][step] = predicted["soc"]
        out["true_temperature_c"][step] = plant.temperature_c
        out["measured_temperature_c"][step] = cyber_measurement["temperature_c"]
        out["twin_temperature_c"][step] = predicted["temperature_c"]
        out["true_voltage_v"][step] = true_v
        out["measured_voltage_v"][step] = cyber_measurement["voltage_v"]
        out["twin_voltage_v"][step] = predicted["voltage_v"]
        out["current_command_a"][step] = current_cmd
        out["cooling_power_w"][step] = cooling_cmd
        out["residual_voltage_v"][step] = r["voltage_v"]
        out["residual_temperature_c"][step] = r["temperature_c"]
        out["residual_soc"][step] = r["soc"]
        out["anomaly_score"][step] = score
        out["anomaly"][step] = float(anomaly)
        out["controller_state"][step] = float(state_code)
        out["packet_received"][step] = float(packet_received)
    return out


def summarize(result: dict[str, np.ndarray]) -> dict[str, float | int]:
    anomaly = result["anomaly"].astype(bool)
    return {
        "samples": int(len(result["time_s"])),
        "anomaly_samples": int(anomaly.sum()),
        "max_anomaly_score": float(np.max(result["anomaly_score"])),
        "max_true_temperature_c": float(np.max(result["true_temperature_c"])),
        "min_true_soc": float(np.min(result["true_soc"])),
        "packet_delivery_fraction": float(np.mean(result["packet_received"])),
        "safe_stop_fraction": float(np.mean(result["controller_state"] == 3)),
    }
