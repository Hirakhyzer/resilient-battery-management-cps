# Security Policy

## Scope

This repository is a software research prototype for simulated battery-management CPS experiments. Security issues may include dependency vulnerabilities, unsafe parsing, secret exposure, CI risks, or flaws that could make the simulation misleading.

It is not a validated BMS, charger, vehicle controller, or battery-safety system.

## Reporting

Do not post sensitive exploit details in a public issue. Use GitHub private vulnerability reporting if enabled. Otherwise contact the maintainer privately through their GitHub profile before public disclosure.

A useful report includes the affected commit, module, impact, reproduction steps, and suggested mitigation.

## Safety boundary

Simulation controller states, thresholds, current commands, cooling commands, attack scenarios, and anomaly-detector logic are illustrative research constructs. They must not be copied into real battery hardware without independent engineering validation, safety review, and cell-specific testing.
