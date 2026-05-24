import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INPUT_SECTIONS = {
    "intent", "structure", "layout", "members", "roof",
    "hub", "bracing", "footings", "joinery"
}


def load_structure(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_structure(data: dict[str, Any], path: str | Path) -> None:
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def seal_section(data: dict[str, Any], section: str) -> None:
    if section not in data:
        raise KeyError(f"Section '{section}' not found in structure")
    data[section]["_sealed"] = True


def assert_not_sealed(data: dict[str, Any], section: str) -> None:
    if data.get(section, {}).get("_sealed"):
        raise RuntimeError(
            f"Section '{section}' is sealed — cannot overwrite. "
            "Downstream stages must not mutate upstream sections."
        )


def compute_source_hash(data: dict[str, Any]) -> str:
    payload = {k: data[k] for k in sorted(INPUT_SECTIONS) if k in data}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
