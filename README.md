# ORBIS Linux

**The World Intelligence Operating System** — an AtDev Linux distribution focused on geospatial exploration, Earth data, environmental analysis, and scientific visualization.

ORBIS is both a **real Debian-based desktop distribution** and a geospatial software platform. The first desktop edition uses Debian 13 Trixie, XFCE, LightDM, and an offline ORBIS Earth viewer.

## Official website\n\nORBIS has an official website served by a Cloudflare Worker. The Worker source is in `cloudflare/worker.js`; deploy it with Wrangler using `wrangler deploy`. The site includes product information, desktop details, project links, roadmap, health endpoint (`/api/status`), `robots.txt`, and sitemap.\n\n## The desktop edition

- Debian 13 Trixie, amd64, live system with installer.
- XFCE desktop, LightDM login, NetworkManager, Firefox ESR.
- Thunar file manager, Mousepad editor, and XFCE Terminal.
- ORBIS wallpaper and system identity.
- ORBIS Earth desktop application for opening and previewing local GeoJSON datasets.
- ORBIS Core CLI installed in an isolated Python virtual environment.

See [Desktop documentation](docs/desktop.md) and [architecture](docs/architecture.md).

## ORBIS Core 0.2.0

The geospatial engine validates common GeoJSON geometry types without third-party runtime dependencies.

```bash
python3 -m pip install -e .
orbis --version
orbis info
orbis doctor
orbis geojson path/to/data.geojson --pretty
pytest
```

The GeoJSON report includes the root type, feature count, geometry counts, coordinate count, and bounding box. Coordinates are interpreted in RFC 7946 order (longitude, latitude). Invalid JSON, unsupported types, non-finite coordinates, out-of-range longitude/latitude, and unclosed polygon rings are rejected.

## Build the desktop ISO

GitHub Actions workflow **Build ORBIS Linux ISO** builds a hybrid amd64 live image. Run it from the Actions tab with workflow_dispatch, or push a change under config/, src/, pyproject.toml, or the workflow file. The ISO and SHA256SUMS are uploaded as a 14-day artifact.

The ISO is not considered released until that workflow completes successfully and the image is smoke-tested in a virtual machine.

## Product roadmap

- **ORBIS Earth** — geographic and Earth-data visualization.
- **ORBIS Maps** — map exploration and geospatial workflows.
- **ORBIS Data** — scientific dataset inspection and validation.
- **ORBIS Weather** — meteorological dataset visualization.
- **ORBIS Sim** — educational environmental simulations.

## Principles
- Debian is the reproducible bootstrap base; no custom kernel is claimed.
- Prefer open formats and documented data sources.
- Support offline workflows where practical.
- Expose data provenance, timestamps, units, and uncertainty.
- Never present stale or simulated data as live observations.

## License
Apache-2.0. See [LICENSE](LICENSE).
