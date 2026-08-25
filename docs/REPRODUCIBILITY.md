# Reproducibility Guide

Use this checklist for every experiment, figure, benchmark, or publication based on this repository.

## Record the software state

Capture the Git commit SHA, Python version, dependency versions, operating system, configuration file, random seed, and exact command used.

## Baseline commands

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
python scripts/run_demo.py --config configs/baseline.json --out results/demo
python scripts/run_scenarios.py
```

## Minimum metadata

For each run, record:

- battery-model parameters and initial SOC/temperature;
- simulation step size and duration;
- current/load profile;
- sensor-noise settings;
- network latency, jitter, and packet-loss settings;
- attack/fault type, magnitude, start time, and duration;
- detector thresholds/persistence;
- controller-state transitions;
- random seed.

## Evaluation metrics

At minimum preserve false-alarm rate, detection rate, detection delay, packet-delivery ratio, time spent in each supervisory state, peak temperature, SOC error, and digital-twin residual statistics when applicable.

## Provenance rules

- Label synthetic results as simulation data.
- Keep measured/recorded battery traces separate from generated traces.
- Cite literature-derived physical parameters.
- Separate tuned detector thresholds from held-out evaluation data.
- Preserve configs and seeds for every reported figure/table.

## Recommended experiment bundle

```text
experiment_name/
├── config.json
├── environment.txt
├── command.txt
├── seed.txt
├── summary.json
├── timeseries.csv
└── figures/
```

A result should be reproducible from a clean checkout of the recorded commit without hidden manual settings.
