from bmscps.battery import BatteryParams, initial_state, step_battery, terminal_voltage_v

def test_discharge_reduces_soc():
    p = BatteryParams(); s = initial_state(p); n = step_battery(p, s, 2.0, 0.0, 10.0)
    assert n.soc < s.soc

def test_terminal_voltage_is_finite():
    p = BatteryParams(); s = initial_state(p)
    assert 2.0 < terminal_voltage_v(p, s, 1.0) < 5.0
