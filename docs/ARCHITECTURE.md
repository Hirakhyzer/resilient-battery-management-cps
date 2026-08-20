# CPS Architecture

The platform separates the system into five inspectable layers:

1. **Physical plant** — reduced-order battery electrical and thermal dynamics.
2. **Sensing** — noisy SOC, terminal-voltage, and temperature measurements.
3. **Communication** — packet loss and discrete latency.
4. **Cyber intelligence** — a digital twin predicts expected behavior; residuals drive anomaly detection.
5. **Supervisory control** — normal, derated, cooling, and simulated safe-stop states.

```text
Battery plant -> sensors -> attack/fault injection -> network -> residual detector
     ^                                                   |              |
     |                                                   v              v
     +--------------- current/cooling <- controller <- digital twin <- measurements
```

The design is intentionally modular so future work can replace the reduced-order plant with PyBaMM, FMI/FMU co-simulation, a hardware-in-the-loop plant, or recorded experimental traces without rewriting the cyber layer.

## Research metrics

Useful system-level metrics include detection delay, false-alarm rate, missed-detection rate, maximum temperature excursion, SOC-estimation error, packet delivery ratio, controller-state occupancy, and performance degradation under combined network/measurement faults.
