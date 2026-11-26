# ORBIS Architecture

## Mission
ORBIS is a specialist operating system for geographic exploration and Earth-science workflows. Its distinguishing feature is the integration of geospatial data tools into a coherent, approachable workstation.

## System layers
1. Base image — initially Debian-based, reproducible, and minimal.
2. ORBIS Core — system identity, diagnostics, configuration, and shared interfaces.
3. Data layer — import, inspect, validate, and document open geospatial datasets.
4. Application layer — Earth, Maps, Data, Weather, and Sim.
5. Desktop layer — consistent navigation, accessibility, and offline-friendly workflows.

## Engineering decisions
- Python powers early developer tools because it is portable and widely available.
- Core CLI commands must work without network access.
- The first release will not claim a custom kernel or independent package ecosystem.
- Debian is a bootstrap base; independence can be evaluated after the core experience is proven.

## Milestones
### M0 — Repository foundation
Project metadata, ORBIS CLI, automated tests, and GitHub Actions CI.

### M1 — Geospatial core
GeoJSON inspection and validation; dataset metadata for provenance, coordinate reference systems, units, and timestamps; licensed sample data.

### M2 — ORBIS Earth
Interactive map/globe prototype and offline sample-data workflow.

### M3 — Bootable system
Reproducible Debian-based image, ORBIS branding, first-boot setup, and QEMU smoke tests.

## Data integrity
Every dataset should expose its source, retrieval time, license, coordinate reference system where applicable, and known limitations. ORBIS must never present stale or simulated data as live observations.
