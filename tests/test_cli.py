from orbis.cli import build_parser, run_info


def test_parser_accepts_info():
    assert build_parser().parse_args(["info"]).command == "info"


def test_parser_accepts_doctor():
    assert build_parser().parse_args(["doctor"]).command == "doctor"


def test_info_reports_unbuilt_image(capsys):
    assert run_info() == 0
    output = capsys.readouterr().out
    assert "ORBIS Linux" in output
    assert "Image status: not built yet" in output
