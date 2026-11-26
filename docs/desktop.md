# ORBIS Desktop

ORBIS Desktop 0.1 is the first graphical system profile.

## Base system
- Debian 13 Trixie (amd64)
- XFCE 4 desktop session
- LightDM display manager
- NetworkManager with its XFCE-friendly applet
- Firefox ESR, Thunar, Mousepad, and XFCE Terminal
- Python 3 runtime for ORBIS tools

The desktop is intentionally lightweight. Large specialist packages such as QGIS are not installed by default; they can be offered as optional software in a later release.

## ORBIS Earth
The first desktop application is an offline GeoJSON viewer. Open a local .geojson or .json file to display its geometry and a coordinate extent. It uses a simple equirectangular plotting view and does not download map tiles, elevation data, or live observations.

Supported geometry display: Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, and GeometryCollection.

This is an early data previewer, not a full GIS replacement. It does not reproject coordinate systems, validate polygon topology, or provide a global basemap.

## Build
The GitHub Actions workflow named "Build ORBIS Linux ISO" builds a hybrid amd64 live ISO and uploads it as a 14-day workflow artifact. Run it manually with workflow_dispatch, or push changes under config/, src/, pyproject.toml, or the workflow itself.

The resulting system is a live environment with a Debian installer. The build workflow must complete successfully before an ISO can be considered available.
