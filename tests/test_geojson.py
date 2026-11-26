import pytest

from orbis.geojson import GeoJSONError, inspect_document


def test_inspects_feature_collection_and_bbox():
    data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"name": "Copiapo"},
             "geometry": {"type": "Point", "coordinates": [-70.33, -27.36]}},
            {"type": "Feature", "properties": None,
             "geometry": {"type": "LineString", "coordinates": [[-71, -27], [-70, -26]]}},
        ],
    }
    result = inspect_document(data)
    assert result["feature_count"] == 2
    assert result["geometry_counts"] == {"LineString": 1, "Point": 1}
    assert result["bbox"] == [-71.0, -27.36, -70.0, -26.0]


def test_accepts_null_geometry():
    result = inspect_document({
        "type": "Feature",
        "properties": None,
        "geometry": None,
    })
    assert result["geometry_counts"] == {"Null": 1}
    assert result["bbox"] is None


@pytest.mark.parametrize("coordinates", [[181, 0], [0, 91], [True, 0], [0, float("inf")]])
def test_rejects_invalid_positions(coordinates):
    with pytest.raises(GeoJSONError):
        inspect_document({"type": "Point", "coordinates": coordinates})


def test_rejects_unclosed_polygon_ring():
    data = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1]]]}
    with pytest.raises(GeoJSONError, match="must be closed"):
        inspect_document(data)


def test_rejects_non_geojson_root():
    with pytest.raises(GeoJSONError, match="unsupported GeoJSON type"):
        inspect_document({"type": "NotGeoJSON"})
