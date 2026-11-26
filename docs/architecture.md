# ORBIS Architecture

## Mission
ORBIS is a specialist desktop operating system for geographic exploration and Earth-science workflows. It combines a usable Linux workstation with integrated geospatial applications.

## System layers
1. **Base image:** Debian 13 Trixie amd64, reproducible live-build configuration.
2. **Desktop:** XFCE, LightDM, NetworkManager, file manager, terminal, and system utilities.
3. **ORBIS Core:** system identity, diagnostics, GeoJSON validation, and shared interfaces.
4. **Data layer:** import, inspect, validate, and document open geospatial datasets.
5. **Applications:** Earth first; Maps, Data, Weather, and Sim as subsequent modules.

## Engineering decisions
- Debian is the bootstrap base; the first release does not claim an independent kernel or package ecosystem.
- XFCE is selected to keep the desktop practical on older computers.
- Python powers early tools because it is portable and widely available.
- Core CLI commands and the first GeoJSON viewer work offline.
- Large specialist software is optional rather than installed in the base image.

## Milestones
### M0 — Repository foundation
Project metadata, ORBIS CLI, automated tests, and GitHub Actions CI.

### M1 — Geospatial core
GeoJSON inspection and validation.

### M2 — ORBIS Earth desktop
Offline GeoJSON viewer with a simple coordinate plot. A full basemap, reprojection, elevation, and 3D globe remain future work.

### M3 — Bootable desktop image
Debian live-build configuration, XFCE session, ORBIS branding, desktop launcher, and ISO build workflow. VM smoke testing is required before release.

## Data integrity
Every dataset should expose its source, retrieval time, license, coordinate reference system where applicable, and known limitations. ORBIS must never present stale or simulated data as live observations.
