def _run_dsm(
    path: Path,
    *,
    response_format: str,
    group_by: str,
    weight: str,
    focus: str | None,
    focus_depth: int,
    package: str | None,
    baseline_path: str | None,
) -> DSMSummary | DSM | DSMDiff | DSMTooLargePayload | DSMErrorPayload:
    """Route archy_dsm between the concise summary, the full matrix, and a diff.

    A diff (baseline_path set) is a deliberate, already-compact comparison
    (new_back_edges is the signal), not a dump, so response_format does not
    apply to it. The full matrix is capped at DEFAULT_MAX_DSM_CELLS cells.
    """
    _validate_response_format(response_format)
    if focus_depth < 0:
        raise ValueError(f"focus_depth must be >= 0; got {focus_depth}")
    graph = _load_graph(path, internal_only=False)
    current = build_dsm(
        graph,
        group_by=cast(GroupBy, group_by),
        weight=cast(Weight, weight),
        focus=focus,
        focus_depth=focus_depth,
        package=package,
    )
