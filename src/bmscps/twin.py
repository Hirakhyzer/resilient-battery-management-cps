"""Digital-twin state predictor and residual calculator."""
from __future__ import annotations
from dataclasses import dataclass
from .battery import BatteryParams, BatteryState, initial_state, step_battery, terminal_voltage_v


@dataclass
class DigitalTwin:
    params: BatteryParams
    state: BatteryState

    @classmethod
    def create(cls, params: BatteryParams) -> "DigitalTwin":
        return cls(params=params, state=initial_state(params))

    def predict(self, current_a: float, cooling_power_w: float, dt_s: float) -> dict[str, float]:
        self.state = step_battery(self.params, self.state, current_a, cooling_power_w, dt_s)
        return {
            "soc": self.state.soc,
            "temperature_c": self.state.temperature_c,
            "voltage_v": terminal_voltage_v(self.params, self.state, current_a),
        }


def residuals(measured: dict[str, float], predicted: dict[str, float]) -> dict[str, float]:
    return {
        "soc": measured["soc"] - predicted["soc"],
        "temperature_c": measured["temperature_c"] - predicted["temperature_c"],
        "voltage_v": measured["voltage_v"] - predicted["voltage_v"],
    }
