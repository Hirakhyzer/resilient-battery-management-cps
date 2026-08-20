#!/usr/bin/env python3
from bmscps.attacks import AttackConfig
from bmscps.network import NetworkConfig
from bmscps.simulation import run_simulation, summarize

SCENARIOS = {
    "normal": (NetworkConfig(packet_loss_probability=0.0, latency_steps=0), AttackConfig(start_step=9999, end_step=10000)),
    "temp_spoof": (NetworkConfig(), AttackConfig(temperature_bias_c=-8.0)),
    "voltage_spoof": (NetworkConfig(), AttackConfig(voltage_bias_v=0.25)),
    "replay": (NetworkConfig(), AttackConfig(replay_measurements=True)),
    "lossy_network": (NetworkConfig(packet_loss_probability=0.25, latency_steps=3), AttackConfig(start_step=9999, end_step=10000)),
}

for name, (network, attack) in SCENARIOS.items():
    print(name, summarize(run_simulation(network=network, attack=attack)))
