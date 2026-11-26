# ORBIS GeoJSON Engine

The initial ORBIS geospatial engine is implemented in `src/orbis/geojson.py`.

## Usage

```bash
orbis geojson datasets/region.geojson
orbis geojson datasets/region.geojson --pretty
```

Exit codes:
- `0`: valid supported GeoJSON; summary printed to stdout.
- `2`: file, JSON, or GeoJSON validation error; diagnostic printed to stderr.

## Summary fields

- `type`: root GeoJSON object type.
- `feature_count`: number of features (zero for bare geometries).
- `geometry_counts`: count of each feature geometry type.
- `coordinate_count`: number of coordinate positions found.
- `bbox`: [west, south, east, north], or null when no coordinates exist.

## Supported objects

Feature, FeatureCollection, GeometryCollection, Point, MultiPoint, LineString, MultiLineString, Polygon, and MultiPolygon. A Feature may have a null geometry.

## Validation

The engine checks object structure, supported types, numeric finite coordinates, longitude and latitude ranges, minimum LineString length, and polygon ring closure/minimum size.

Coordinates are interpreted as longitude then latitude, consistent with RFC 7946. Additional coordinate dimensions are accepted but not included in the 2D bounding box.

## Current limitations

This is structural validation, not full GIS topology validation. It does not reproject coordinates, verify polygon self-intersections, resolve CRS metadata, download basemaps, or claim that a dataset is scientifically accurate. Bounding boxes are simple min/max bounds and do not specially handle geometries crossing the antimeridian.
