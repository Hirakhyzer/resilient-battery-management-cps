#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import matplotlib.pyplot as plt
from bmscps.attacks import AttackConfig
from bmscps.battery import BatteryParams
from bmscps.controller import ControllerConfig
from bmscps.detector import DetectorConfig
from bmscps.network import NetworkConfig
from bmscps.simulation import SimulationConfig, run_simulation, summarize


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/baseline.json")
    ap.add_argument("--out", default="results/demo")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text())
    result = run_simulation(
        BatteryParams(**cfg.get("battery", {})),
        SimulationConfig(**cfg.get("simulation", {})),
        NetworkConfig(**cfg.get("network", {})),
        AttackConfig(**cfg.get("attack", {})),
        DetectorConfig(**cfg.get("detector", {})),
        ControllerConfig(**cfg.get("controller", {})),
    )
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    keys = list(result)
    with (out / "timeseries.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(keys)
        for i in range(len(result[keys[0]])):
            w.writerow([result[k][i] for k in keys])
    (out / "summary.json").write_text(json.dumps(summarize(result), indent=2))

    plt.figure(figsize=(9, 4))
    plt.plot(result["time_s"], result["measured_temperature_c"], label="measured")
    plt.plot(result["time_s"], result["twin_temperature_c"], label="digital twin")
    plt.xlabel("Time (s)"); plt.ylabel("Temperature (°C)"); plt.legend(); plt.tight_layout()
    plt.savefig(out / "temperature_twin.png", dpi=160); plt.close()

    plt.figure(figsize=(9, 4))
    plt.plot(result["time_s"], result["anomaly_score"], label="anomaly score")
    plt.plot(result["time_s"], result["controller_state"], label="controller state")
    plt.xlabel("Time (s)"); plt.legend(); plt.tight_layout()
    plt.savefig(out / "resilience_response.png", dpi=160); plt.close()
    print(json.dumps(summarize(result), indent=2))

if __name__ == "__main__":
    main()
