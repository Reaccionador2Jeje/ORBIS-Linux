"""Small, dependency-free GeoJSON reader and validator.

Coordinates follow RFC 7946 order: longitude, latitude (and optional altitude).
This module intentionally validates the common GeoJSON object and geometry types;
it does not attempt topology validation or coordinate reprojection.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


class GeoJSONError(ValueError):
    """Raised when a document is not valid supported GeoJSON."""


_GEOMETRY_TYPES = {
    "Point", "MultiPoint", "LineString", "MultiLineString",
    "Polygon", "MultiPolygon", "GeometryCollection",
}


def _position(value: Any, path: str) -> tuple[float, float]:
    if not isinstance(value, list) or len(value) < 2:
        raise GeoJSONError(f"{path}: position must be an array with at least 2 numbers")
    if any(isinstance(n, bool) or not isinstance(n, (int, float)) for n in value):
        raise GeoJSONError(f"{path}: coordinates must be numeric")
    if not all(math.isfinite(float(n)) for n in value):
        raise GeoJSONError(f"{path}: coordinates must be finite")
    lon, lat = float(value[0]), float(value[1])
    if not -180 <= lon <= 180:
        raise GeoJSONError(f"{path}: longitude {lon} is outside [-180, 180]")
    if not -90 <= lat <= 90:
        raise GeoJSONError(f"{path}: latitude {lat} is outside [-90, 90]")
    return lon, lat


def _positions(value: Any, path: str, depth: int) -> list[tuple[float, float]]:
    if depth == 0:
        return [_position(value, path)]
    if not isinstance(value, list) or not value:
        raise GeoJSONError(f"{path}: coordinate array must not be empty")
    points: list[tuple[float, float]] = []
    for index, child in enumerate(value):
        points.extend(_positions(child, f"{path}[{index}]", depth - 1))
    return points


def _geometry(obj: Any, path: str = "geometry") -> tuple[str, list[tuple[float, float]]]:
    if obj is None:
        return "Null", []
    if not isinstance(obj, dict):
        raise GeoJSONError(f"{path}: geometry must be an object or null")
    kind = obj.get("type")
    if kind not in _GEOMETRY_TYPES:
        raise GeoJSONError(f"{path}: unsupported geometry type {kind!r}")
    if kind == "GeometryCollection":
        geometries = obj.get("geometries")
        if not isinstance(geometries, list):
            raise GeoJSONError(f"{path}.geometries: expected an array")
        points: list[tuple[float, float]] = []
        for i, child in enumerate(geometries):
            _, child_points = _geometry(child, f"{path}.geometries[{i}]")
            points.extend(child_points)
        return kind, points

    depths = {
        "Point": 0, "MultiPoint": 1, "LineString": 1,
        "MultiLineString": 2, "Polygon": 2, "MultiPolygon": 3,
    }
    points = _positions(obj.get("coordinates"), f"{path}.coordinates", depths[kind])
    if kind == "LineString" and len(points) < 2:
        raise GeoJSONError(f"{path}: LineString requires at least 2 positions")
    if kind == "Polygon":
        _validate_rings(obj["coordinates"], path)
    if kind == "MultiPolygon":
        for polygon_index, polygon in enumerate(obj["coordinates"]):
            _validate_rings(polygon, f"{path}.coordinates[{polygon_index}]")
    return kind, points


def _validate_rings(rings: Any, path: str) -> None:
    if not isinstance(rings, list) or not rings:
        raise GeoJSONError(f"{path}: Polygon requires at least one linear ring")
    for i, ring in enumerate(rings):
        if not isinstance(ring, list) or len(ring) < 4:
            raise GeoJSONError(f"{path}: ring {i} requires at least 4 positions")
        if ring[0] != ring[-1]:
            raise GeoJSONError(f"{path}: ring {i} must be closed")


def _feature(obj: Any, path: str) -> tuple[str, list[tuple[float, float]]]:
    if not isinstance(obj, dict) or obj.get("type") != "Feature":
        raise GeoJSONError(f"{path}: expected a GeoJSON Feature")
    properties = obj.get("properties")
    if properties is not None and not isinstance(properties, dict):
        raise GeoJSONError(f"{path}.properties: expected an object or null")
    if "geometry" not in obj:
        raise GeoJSONError(f"{path}: missing geometry member")
    kind, points = _geometry(obj["geometry"], f"{path}.geometry")
    return kind, points


def inspect_document(document: Any) -> dict[str, Any]:
    """Validate a GeoJSON object and return a compact, JSON-safe summary."""
    if not isinstance(document, dict):
        raise GeoJSONError("root: expected a GeoJSON object")
    kind = document.get("type")
    counts: Counter[str] = Counter()
    points: list[tuple[float, float]] = []

    if kind == "Feature":
        geometry_type, points = _feature(document, "feature")
        counts[geometry_type] += 1
        feature_count = 1
    elif kind == "FeatureCollection":
        features = document.get("features")
        if not isinstance(features, list):
            raise GeoJSONError("features: expected an array")
        feature_count = len(features)
        for i, feature in enumerate(features):
            geometry_type, feature_points = _feature(feature, f"features[{i}]")
            counts[geometry_type] += 1
            points.extend(feature_points)
    elif kind in _GEOMETRY_TYPES:
        geometry_type, points = _geometry(document, "geometry")
        counts[geometry_type] += 1
        feature_count = 0
    else:
        raise GeoJSONError(f"root.type: unsupported GeoJSON type {kind!r}")

    bounds = None
    if points:
        longitudes = [p[0] for p in points]
        latitudes = [p[1] for p in points]
        bounds = [
            min(longitudes), min(latitudes),
            max(longitudes), max(latitudes),
        ]

    return {
        "type": kind,
        "feature_count": feature_count,
        "geometry_counts": dict(sorted(counts.items())),
        "coordinate_count": len(points),
        "bbox": bounds,
    }


def inspect_file(filename: str | Path) -> dict[str, Any]:
    """Load and inspect a UTF-8 GeoJSON file."""
    path = Path(filename)
    try:
        with path.open("r", encoding="utf-8") as stream:
            document = json.load(stream)
    except OSError as exc:
        raise GeoJSONError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise GeoJSONError(f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    return inspect_document(document)
