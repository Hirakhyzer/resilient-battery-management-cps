# Research Roadmap

## Phase 1 — Reproducible baseline
Validate numerical stability, parameter provenance, and sensitivity of the reduced-order electrical/thermal plant.

## Phase 2 — Digital-twin estimation
Compare open-loop prediction, observer-based estimation, and parameter adaptation. Quantify SOC and temperature prediction uncertainty.

## Phase 3 — CPS resilience
Run factorial experiments over packet loss, delay, sensor noise, spoof magnitude, replay duration, and simultaneous faults. Measure detection delay and closed-loop degradation.

## Phase 4 — Physics-informed anomaly detection
Compare threshold residuals with statistical detectors and lightweight ML using residual features. Keep a physics-only baseline for interpretability.

## Phase 5 — Fault-tolerant control
Study graceful degradation policies under uncertain telemetry and explicitly evaluate false positives versus unnecessary derating.

## Phase 6 — Hardware-in-the-loop
Replace the simulated plant with a safe real-time battery emulator or recorded hardware traces. Keep the cyber/network/controller interface unchanged.

## Phase 7 — Reproducible research package
Add calibrated datasets, experiment manifests, confidence intervals, ablation studies, and release-tagged results suitable for a paper artifact.
