from bmscps.detector import DetectorConfig, ResidualDetector

def test_persistent_residual_triggers():
    d = ResidualDetector(DetectorConfig(persistence_steps=2))
    r = {"voltage_v": 0.2, "temperature_c": 0.0, "soc": 0.0}
    assert d.update(r)[0] is False
    assert d.update(r)[0] is True

def test_normal_residual_does_not_trigger():
    d = ResidualDetector(DetectorConfig())
    for _ in range(10):
        assert d.update({"voltage_v": 0.01, "temperature_c": 0.1, "soc": 0.001})[0] is False
