# ORBIS Linux

**The World Intelligence Operating System** — an AtDev Linux distribution focused on geospatial exploration, Earth data, environmental analysis, and scientific visualization.

> Early-stage project: ORBIS Core now includes a working GeoJSON inspection engine. A bootable Linux image and graphical desktop are not yet available.

## Vision
- **ORBIS Earth** — geographic and Earth-data visualization.
- **ORBIS Maps** — map exploration and geospatial workflows.
- **ORBIS Data** — scientific dataset inspection and validation.
- **ORBIS Weather** — meteorological dataset visualization.
- **ORBIS Sim** — educational environmental simulations.
- **ORBIS Desktop** — a cohesive specialist workstation.

## ORBIS Core 0.2.0

The first geospatial engine validates common GeoJSON geometry types without third-party runtime dependencies.

```bash
python3 -m pip install -e .
orbis --version
orbis info
orbis doctor
orbis geojson path/to/data.geojson --pretty
pytest
```

The GeoJSON report includes the root type, feature count, geometry counts, coordinate count, and bounding box. Coordinates are interpreted in RFC 7946 order (longitude, latitude). Invalid JSON, unsupported types, non-finite coordinates, out-of-range longitude/latitude, and unclosed polygon rings are rejected.

## Principles
- Start with a reproducible Debian-based image while keeping ORBIS tools portable.
- Prefer open formats and documented data sources.
- Support offline workflows where practical.
- Expose data provenance, timestamps, units, and uncertainty.
- Keep specialist applications modular.
- Never present stale or simulated data as live observations.

## Development status
- M0 — repository foundation and CLI: implemented.
- M1 — GeoJSON inspection and validation: initial implementation.
- M2 — interactive ORBIS Earth prototype: planned.
- M3 — reproducible bootable image and QEMU smoke tests: planned.

## License
Apache-2.0. See [LICENSE](LICENSE).
