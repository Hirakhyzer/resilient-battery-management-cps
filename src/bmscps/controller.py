"""Fault-aware supervisory controller for the simulated battery CPS."""
from __future__ import annotations
from dataclasses import dataclass

NORMAL = 0
DERATE = 1
COOL = 2
SAFE_STOP = 3
STATE_NAMES = {NORMAL: "NORMAL", DERATE: "DERATE", COOL: "COOL", SAFE_STOP: "SAFE_STOP"}


@dataclass(frozen=True)
class ControllerConfig:
    warm_temperature_c: float = 32.0
    hot_temperature_c: float = 38.0
    max_temperature_c: float = 43.0
    nominal_current_a: float = 2.0
    derated_current_a: float = 1.0
    cooling_power_w: float = 1.5


def control(measured_temp_c: float, anomaly: bool, cfg: ControllerConfig) -> tuple[int, float, float]:
    """Return state, current command, and abstract cooling command.

    SAFE_STOP is a simulation state only; it is not a real battery safety procedure.
    """
    if anomaly or measured_temp_c >= cfg.max_temperature_c:
        return SAFE_STOP, 0.0, cfg.cooling_power_w
    if measured_temp_c >= cfg.hot_temperature_c:
        return COOL, cfg.derated_current_a, cfg.cooling_power_w
    if measured_temp_c >= cfg.warm_temperature_c:
        return DERATE, cfg.derated_current_a, 0.0
    return NORMAL, cfg.nominal_current_a, 0.0
