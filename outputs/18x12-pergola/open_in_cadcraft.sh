#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$DIR/../.."
DXF="$DIR/cad/SB01-structure.dxf"
echo "Opening $DXF in Cadcraft..."
if [ -f "$REPO_ROOT/vendor/cadcraft/target/debug/cadcraft" ]; then
    "$REPO_ROOT/vendor/cadcraft/target/debug/cadcraft" "$DXF"
elif [ -f "$REPO_ROOT/vendor/cadcraft/target/release/cadcraft" ]; then
    "$REPO_ROOT/vendor/cadcraft/target/release/cadcraft" "$DXF"
else
    cargo run --manifest-path "$REPO_ROOT/vendor/cadcraft/Cargo.toml" -p cadcraft -- "$DXF"
fi
