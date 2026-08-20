"""Reduced-order lithium-ion battery plant model for CPS simulation.

The equations are intentionally compact and intended for software experiments,
state-estimation studies, and fault-injection research. They are not a cell-safety
model and must not be used to set real charging limits.
"""
from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BatteryParams:
    capacity_ah: float = 2.5
    nominal_voltage_v: float = 3.7
    internal_resistance_ohm: float = 0.055
    rc_resistance_ohm: float = 0.018
    rc_capacitance_f: float = 2400.0
    thermal_capacity_j_k: float = 520.0
    thermal_resistance_k_w: float = 5.0
    ambient_temperature_c: float = 25.0
    initial_soc: float = 0.80
    initial_temperature_c: float = 25.0


@dataclass
class BatteryState:
    soc: float
    v_rc: float
    temperature_c: float


def initial_state(params: BatteryParams) -> BatteryState:
    _validate_params(params)
    return BatteryState(params.initial_soc, 0.0, params.initial_temperature_c)


def _validate_params(p: BatteryParams) -> None:
    if p.capacity_ah <= 0 or p.internal_resistance_ohm <= 0:
        raise ValueError("capacity and resistance must be positive")
    if p.rc_resistance_ohm <= 0 or p.rc_capacitance_f <= 0:
        raise ValueError("RC parameters must be positive")
    if p.thermal_capacity_j_k <= 0 or p.thermal_resistance_k_w <= 0:
        raise ValueError("thermal parameters must be positive")
    if not 0 <= p.initial_soc <= 1:
        raise ValueError("initial_soc must be between 0 and 1")


def open_circuit_voltage_v(soc: float) -> float:
    """Smooth illustrative OCV curve for normalized SOC in [0, 1]."""
    s = min(1.0, max(0.0, soc))
    return 3.0 + 1.15 * s + 0.05 * math.tanh(8.0 * (s - 0.5))


def terminal_voltage_v(params: BatteryParams, state: BatteryState, current_a: float) -> float:
    """Terminal voltage. Positive current means discharge."""
    return open_circuit_voltage_v(state.soc) - state.v_rc - current_a * params.internal_resistance_ohm


def step_battery(
    params: BatteryParams,
    state: BatteryState,
    current_a: float,
    cooling_power_w: float,
    dt_s: float,
) -> BatteryState:
    """Advance the battery plant by one Euler step.

    Positive current discharges the cell. Cooling power is an abstract non-negative
    heat-removal command used only in simulation.
    """
    _validate_params(params)
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    if cooling_power_w < 0:
        raise ValueError("cooling_power_w must be non-negative")

    dsoc = -(current_a * dt_s) / (params.capacity_ah * 3600.0)
    soc = min(1.0, max(0.0, state.soc + dsoc))

    tau_rc = params.rc_resistance_ohm * params.rc_capacitance_f
    dvrc = (-state.v_rc + current_a * params.rc_resistance_ohm) * dt_s / tau_rc
    v_rc = state.v_rc + dvrc

    joule_heat_w = (current_a ** 2) * params.internal_resistance_ohm
    passive_heat_w = (state.temperature_c - params.ambient_temperature_c) / params.thermal_resistance_k_w
    dtemp = (joule_heat_w - passive_heat_w - cooling_power_w) * dt_s / params.thermal_capacity_j_k
    temperature_c = state.temperature_c + dtemp
    return BatteryState(soc=soc, v_rc=v_rc, temperature_c=temperature_c)
