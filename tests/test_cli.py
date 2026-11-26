from orbis.cli import build_parser, run_info


def test_parser_accepts_info():
    assert build_parser().parse_args(["info"]).command == "info"


def test_parser_accepts_doctor():
    assert build_parser().parse_args(["doctor"]).command == "doctor"


def test_parser_accepts_geojson():
    args = build_parser().parse_args(["geojson", "sample.geojson", "--pretty"])
    assert args.command == "geojson"
    assert args.file == "sample.geojson"
    assert args.pretty is True


def test_info_reports_geospatial_engine(capsys):
    assert run_info() == 0
    output = capsys.readouterr().out
    assert "ORBIS Linux" in output
    assert "GeoJSON inspection enabled" in output
    assert "Image status: not built yet" in output
