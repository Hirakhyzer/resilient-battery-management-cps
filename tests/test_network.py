from bmscps.network import NetworkChannel, NetworkConfig

def test_zero_loss_delivery_with_latency():
    c = NetworkChannel(NetworkConfig(packet_loss_probability=0.0, latency_steps=2))
    c.send(0, {"x": 1.0})
    assert c.receive(0) is None
    assert c.receive(1) is None
    assert c.receive(2) == {"x": 1.0}
