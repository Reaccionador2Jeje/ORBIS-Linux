import pytest

from orbis.geojson import GeoJSONError, inspect_document


def test_inspects_geometry_collection():
    data = {
        "type": "GeometryCollection",
        "geometries": [
            {"type": "Point", "coordinates": [12, 34]},
            {"type": "LineString", "coordinates": [[10, 20], [11, 21]]},
        ],
    }
    report = inspect_document(data)
    assert report["coordinate_count"] == 3
    assert report["bbox"] == [10.0, 20.0, 12.0, 34.0]


def test_rejects_multiline_with_one_position():
    data = {"type": "MultiLineString", "coordinates": [[[1, 2]]]}
    with pytest.raises(GeoJSONError, match="MultiLineString"):
        inspect_document(data)


def test_rejects_non_string_geometry_type():
    data = {"type": "Feature", "properties": {}, "geometry": {"type": [], "coordinates": []}}
    with pytest.raises(GeoJSONError, match="unsupported geometry"):
        inspect_document(data)
