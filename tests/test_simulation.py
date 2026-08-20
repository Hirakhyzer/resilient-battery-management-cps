import numpy as np
from bmscps.attacks import AttackConfig
from bmscps.network import NetworkConfig
from bmscps.simulation import SimulationConfig, run_simulation, summarize

def test_simulation_shapes():
    r = run_simulation(sim=SimulationConfig(steps=40), network=NetworkConfig(packet_loss_probability=0.0, latency_steps=0), attack=AttackConfig(start_step=999, end_step=1000))
    assert len(r["time_s"]) == 40
    assert np.isfinite(r["true_voltage_v"]).all()

def test_temperature_spoof_detected():
    r = run_simulation(sim=SimulationConfig(steps=100), network=NetworkConfig(packet_loss_probability=0.0, latency_steps=0), attack=AttackConfig(start_step=20, end_step=60, temperature_bias_c=8.0))
    assert r["anomaly"].sum() > 0
    assert summarize(r)["max_anomaly_score"] > 1.0
