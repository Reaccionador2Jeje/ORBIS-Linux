# ORBIS Linux

**The World Intelligence Operating System** — an AtDev Linux distribution focused on geospatial exploration, Earth data, environmental analysis, and scientific visualization.

> Early-stage project: this repository currently contains the developer foundation, not a bootable Linux image.

## Vision
- ORBIS Earth — geographic and Earth-data visualization.
- ORBIS Maps — map exploration and geospatial workflows.
- ORBIS Data — scientific dataset inspection and validation.
- ORBIS Weather — meteorological dataset visualization.
- ORBIS Sim — educational environmental simulations.
- ORBIS Desktop — a cohesive specialist workstation.

## Principles
- Begin with a reproducible Debian-based image while keeping ORBIS tools portable.
- Prefer open formats and documented data sources.
- Support offline workflows where practical.
- Expose data provenance, timestamps, units, and uncertainty.
- Keep specialist applications modular.

## Current milestone
M0 establishes ORBIS Core: a small Python CLI, tests, and automated CI. Image building and graphical applications come later.

## Development
Requires Python 3.10+.
    python3 -m pip install -e .
    orbis --help
    orbis info
    orbis doctor
    pytest

## License
Apache-2.0. See LICENSE.
