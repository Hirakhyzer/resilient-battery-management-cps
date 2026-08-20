# Threat and Fault Model

This repository is for defensive CPS research. The fault injector models effects on the simulated measurement channel rather than providing instructions for compromising real BMS hardware.

## Included scenarios

- temperature measurement bias/spoofing;
- voltage measurement bias/spoofing;
- replay of an earlier measurement snapshot;
- packet loss;
- communication latency;
- ordinary sensor noise.

## Defender assumptions

The controller has a physics-based digital twin, observes delayed/lossy telemetry, and can respond by changing an abstract current command and cooling command in simulation.

## Out of scope

The repository does not model real vehicle CAN message identifiers, real charging protocols, bypass procedures, cell-abuse experiments, or instructions for defeating physical battery protection systems.
