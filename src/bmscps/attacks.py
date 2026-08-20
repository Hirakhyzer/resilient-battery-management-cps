"""Deterministic fault and cyberattack injection for defensive CPS experiments."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class AttackConfig:
    start_step: int = 120
    end_step: int = 220
    temperature_bias_c: float = 0.0
    voltage_bias_v: float = 0.0
    replay_measurements: bool = False


def apply_attack(
    measurement: dict[str, float],
    step: int,
    config: AttackConfig,
    replay_buffer: dict[str, float] | None,
) -> dict[str, float]:
    attacked = dict(measurement)
    active = config.start_step <= step < config.end_step
    if not active:
        return attacked
    if config.replay_measurements and replay_buffer is not None:
        return dict(replay_buffer)
    attacked["temperature_c"] += config.temperature_bias_c
    attacked["voltage_v"] += config.voltage_bias_v
    return attacked
