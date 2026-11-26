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

## ORBIS Installer
ORBIS uses a customized Calamares graphical installer. Debian Installer is explicitly disabled in the live-build configuration.

The live desktop exposes **Install ORBIS Linux** in the applications menu and on the desktop. Calamares copies the live SquashFS filesystem to the selected target, configures the installed system, creates a normal user account, and installs GRUB for the detected boot mode.

Partitioning starts with no destructive action selected. The user must explicitly choose and confirm the target disk and partition layout. Back up important data before installing an operating system.

The installer configuration lives under `config/includes.chroot/etc/calamares/`; ORBIS branding is in `branding/orbis/`.

## Build
The GitHub Actions workflow named "Build ORBIS Linux ISO" builds a hybrid amd64 live ISO and publishes the ISO plus SHA256SUMS as a GitHub Release after a successful build. Run it manually with workflow_dispatch, or push changes under config/, src/, pyproject.toml, or the workflow itself.

An ISO is not considered available until the workflow completes successfully and the image is smoke-tested in a virtual machine.
