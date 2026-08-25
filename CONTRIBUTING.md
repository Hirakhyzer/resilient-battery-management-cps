# Contributing

Contributions are welcome when they improve reproducibility, battery/CPS modeling, anomaly detection, resilience experiments, tests, or documentation.

## Pull-request checklist

1. Keep changes focused and explain the research question or engineering reason.
2. Run `pytest` and the relevant scenario/demo scripts.
3. Add tests for changed behavior.
4. Record units and provenance for every physical parameter.
5. Use deterministic seeds for stochastic experiments unless randomness itself is under study.
6. Distinguish synthetic simulation output from measured battery data.

## Model changes

For electrical, thermal, SOC, or digital-twin changes, document equations, assumptions, valid operating range, parameter source, and known limitations. Do not imply that the reduced-order model is validated for a real cell unless calibration evidence is provided.

## Security and resilience experiments

Attack/fault scenarios must remain simulation-only and defensive in purpose. Prefer abstract manipulations such as sensor bias, replay, packet loss, or latency rather than protocol-specific exploitation. Report detection thresholds, attack windows, random seeds, and evaluation metrics.

## Safety

Do not contribute real charging limits, protection thresholds, or actuator settings presented as deployment-ready guidance. Hardware-in-the-loop work should use a safe emulator or appropriately supervised laboratory setup.
