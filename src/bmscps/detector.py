"""Transparent residual-based anomaly detector."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DetectorConfig:
    voltage_threshold_v: float = 0.12
    temperature_threshold_c: float = 2.5
    soc_threshold: float = 0.06
    persistence_steps: int = 3


class ResidualDetector:
    def __init__(self, config: DetectorConfig):
        if min(config.voltage_threshold_v, config.temperature_threshold_c, config.soc_threshold) <= 0:
            raise ValueError("thresholds must be positive")
        if config.persistence_steps <= 0:
            raise ValueError("persistence_steps must be positive")
        self.config = config
        self._count = 0

    def update(self, r: dict[str, float]) -> tuple[bool, float]:
        score = max(
            abs(r["voltage_v"]) / self.config.voltage_threshold_v,
            abs(r["temperature_c"]) / self.config.temperature_threshold_c,
            abs(r["soc"]) / self.config.soc_threshold,
        )
        self._count = self._count + 1 if score >= 1.0 else 0
        return self._count >= self.config.persistence_steps, float(score)
