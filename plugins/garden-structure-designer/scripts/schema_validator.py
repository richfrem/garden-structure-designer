#!/usr/bin/env python3
"""
schema_validator.py
===================

Purpose:
    Validates every staging ``*.json`` that has a matching ``<stem>.schema.json`` in the schemas
    directory (draft-07) and runs the cross-section member-count invariant on structure.json
    (``invariants.member_counts_match_sections``: primary rafters and CAD node counts equal
    layout.post_count). ``--strict`` warns about unknown top-level keys in structure.json. The
    report (``--json-output``, consumed by the red-team gate) is bound to structure.json's
    ``source_hash`` and revision identity so stale evidence is detectable.

Layer: Execution / Stage 0-3 Schema Gate

Key Input Dependencies:
    - context/staging/*.json and plugins/garden-structure-designer/schemas/*.schema.json
    - structure.schema.json carries the C1 meta fields (topology_family, revision_id, revision_hash)
    - jsonschema, path_utils.py

Key Functions:
    main() -> None
    load_json(path) -> dict
    validate_files(target_path, schema_path, strict) -> tuple[list[dict], str]
    check_member_counts(structure_file) -> list[dict]
    build_report(files, status, structure_file) -> dict

Usage Examples:
    python3 schema_validator.py [staging_dir] [schema_dir] [--strict] [--json-output report.json]
"""
import json
import sys
import jsonschema
from pathlib import Path
import argparse

sys.path.append(str(Path(__file__).parent.resolve()))
from path_utils import staging_dir, schemas_dir

def load_json(path) -> dict:
    """Reads a JSON file."""
    with open(path) as f: return json.load(f)


SKIPPED_FILES = ("repair-report.json", "drift_report.json", "learning-registry.json", "script-run-history.jsonl")


def validate_files(target_path: Path, schema_path: Path, strict: bool) -> tuple[list[dict], str]:
    """Schema-validates each staging JSON that has a schema; returns (per-file reports, PASS/WARNING/FAIL)."""
    overall_status = "PASS"
    files: list[dict] = []
    for file in target_path.glob("*.json"):
        schema_file = schema_path / f"{file.stem}.schema.json"
        if file.name in SKIPPED_FILES or not schema_file.exists():
            continue
        data, schema = load_json(file), load_json(schema_file)
        file_report = {"path": str(file), "schema": str(schema_file), "status": "PASS", "errors": [], "warnings": []}
        try:
            jsonschema.validate(data, schema)
            unknown = set(data.keys()) - set(schema.get("properties", {}).keys()) if strict and file.name == "structure.json" else set()
            if unknown:
                file_report["warnings"].append(f"Unknown keys in structure.json: {unknown}")
                file_report["status"] = "WARNING"
                overall_status = "WARNING" if overall_status == "PASS" else overall_status
        except jsonschema.ValidationError as e:
            file_report["status"] = "FAIL"
            file_report["errors"].append(e.message)
            overall_status = "FAIL"
        files.append(file_report)
    return files, overall_status


def check_member_counts(structure_file: Path) -> list[dict]:
    """Cross-section invariant: when declared, rafter and CAD node counts must equal layout.post_count."""
    if not structure_file.exists():
        return []
    s = load_json(structure_file)
    post_count = s.get("layout", {}).get("post_count")
    if not (s.get("invariants", {}).get("member_counts_match_sections") and post_count):
        return []

    def failure(detail: str) -> dict:
        return {"path": str(structure_file), "check": "member_counts_match_sections", "status": "FAIL", "detail": detail}

    failures = []
    rafter_count = s.get("roof", {}).get("primary_rafters", {}).get("count")
    if rafter_count is not None and rafter_count != post_count:
        failures.append(failure(f"rafter count {rafter_count} != post_count {post_count}"))
    cad_nodes = s.get("cad", {}).get("nodes", {})
    for key in ("post_bases", "post_tops", "beam_ring"):
        actual = len(cad_nodes.get(key, []))
        if cad_nodes and actual and actual != post_count:
            failures.append(failure(f"cad.nodes.{key} length {actual} != post_count {post_count}"))
    return failures


def build_report(files: list[dict], status: str, structure_file: Path) -> dict:
    """Assembles the schema-validation report, bound to structure.json's source hash and revision."""
    meta = (load_json(structure_file).get("meta") or {}) if structure_file.exists() else {}
    return {
        "schema": "garden-structure-designer/schema-validation-report/1.1",
        "status": status,
        "source_hash": meta.get("source_hash"),
        "revision_id": meta.get("revision_id"),
        "revision_hash": meta.get("revision_hash"),
        "files": files,
    }


def main() -> None:
    """CLI entrypoint: validate staging JSON against the schemas, write the report, exit 1 on FAIL."""
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir", nargs='?', default=str(staging_dir()))
    parser.add_argument("schema_dir", nargs='?', default=str(schemas_dir()))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-output", type=str)
    args = parser.parse_args()

    target_path = Path(args.target_dir)
    files, overall_status = validate_files(target_path, Path(args.schema_dir), args.strict)
    count_failures = check_member_counts(target_path / "structure.json")
    files.extend(count_failures)
    if count_failures:
        overall_status = "FAIL"

    report = build_report(files, overall_status, target_path / "structure.json")
    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(report, f, indent=2)

    if overall_status == "FAIL":
        print("SCHEMA VALIDATION FAILED")
        for f in report["files"]:
            if f.get("errors"): print(f"  {f['path']}: {f['errors']}")
            elif f.get("detail"): print(f"  {f['path']}: {f['detail']}")
        sys.exit(1)
    print(f"SCHEMA VALIDATION PASSED ✓ ({overall_status})")
    sys.exit(0)


if __name__ == "__main__":
    main()
