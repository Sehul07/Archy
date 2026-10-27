def test_run_cycles_min_size_rejects_invalid_values(tmp_path: Path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "a.py").write_text("from pkg.b import thing\n")
    (pkg / "b.py").write_text("from pkg.a import thing\n")

    with pytest.raises(ValueError, match=r"min_size must be >= 1; got 0"):
        _run_cycles(tmp_path, min_size=0, internal_only=True)
    with pytest.raises(ValueError, match=r"min_size must be >= 1; got -5"):
        _run_cycles(tmp_path, min_size=-5, internal_only=True)

    assert len(_run_cycles(tmp_path, min_size=1, internal_only=True)) == 1


def test_run_dsm_focus_depth_rejects_invalid_values(tmp_path: Path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "a.py").write_text("from pkg.b import thing\n")
    (pkg / "b.py").write_text("")

    with pytest.raises(ValueError, match=r"focus_depth must be >= 0; got -1"):
        _run_dsm(
            tmp_path,
            response_format="summary",
            group_by="community",
            weight="imports",
            focus="pkg.a",
            focus_depth=-1,
            package=None,
            baseline_path=None,
        )

    summary = _run_dsm(
        tmp_path,
        response_format="summary",
        group_by="community",
        weight="imports",
        focus="pkg.a",
        focus_depth=0,
        package=None,
        baseline_path=None,
    )
    assert isinstance(summary, DSMSummary)
