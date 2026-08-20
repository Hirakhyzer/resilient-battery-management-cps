"""Simple packet-loss and latency model for CPS telemetry."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class NetworkConfig:
    packet_loss_probability: float = 0.02
    latency_steps: int = 1
    random_seed: int = 7


def validate_network(cfg: NetworkConfig) -> None:
    if not 0 <= cfg.packet_loss_probability <= 1:
        raise ValueError("packet_loss_probability must be between 0 and 1")
    if cfg.latency_steps < 0:
        raise ValueError("latency_steps must be non-negative")


class NetworkChannel:
    def __init__(self, config: NetworkConfig):
        validate_network(config)
        self.config = config
        self.rng = np.random.default_rng(config.random_seed)
        self.queue: list[tuple[int, dict[str, float]]] = []

    def send(self, step: int, packet: dict[str, float]) -> None:
        if self.rng.random() < self.config.packet_loss_probability:
            return
        self.queue.append((step + self.config.latency_steps, dict(packet)))

    def receive(self, step: int) -> dict[str, float] | None:
        for i, (arrival, packet) in enumerate(self.queue):
            if arrival <= step:
                self.queue.pop(i)
                return packet
        return None
