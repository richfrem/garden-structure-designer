import sys
import argparse
from pathlib import Path

# Add script directory to sys.path to allow importing local modules
script_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(script_dir))

from structure_io import load_structure, save_structure
from path_utils import staging_dir

def main():
    parser = argparse.ArgumentParser(description="Reset derived sections of structure.json")
    parser.add_argument("model_path", nargs="?", default=str(staging_dir() / "structure.json"), help="Path to structure.json")
    parser.add_argument("--geometry", action="store_true", help="Reset geometry section")
    parser.add_argument("--cad", action="store_true", help="Reset cad section")
    parser.add_argument("--lifecycle", default="ENGINEERED", help="Reset lifecycle to this state")
    
    args = parser.parse_args()
    
    model_path = Path(args.model_path)
    if not model_path.exists():
        print(f"Error: {model_path} not found.")
        sys.exit(1)
        
    data = load_structure(model_path)
    
    changed = False
    if args.geometry and "geometry" in data:
        data["geometry"]["_sealed"] = False
        changed = True
        
    if args.cad and "cad" in data:
        data["cad"]["_sealed"] = False
        changed = True
        
    if "meta" in data and data["meta"].get("lifecycle") != args.lifecycle:
        data["meta"]["lifecycle"] = args.lifecycle
        changed = True
        
    if changed:
        save_structure(data, model_path)
        print(f"Reset derived sections in {model_path.name}. Lifecycle set to {args.lifecycle}.")
        
        # Optionally remove shim generated files to prevent stale state issues
        staging_dir = model_path.parent
        for legacy_file in ["structural-model.json", "geometry-calculations.json", "design-spec.json"]:
            legacy_path = staging_dir / legacy_file
            if legacy_path.exists():
                legacy_path.unlink()
                print(f"Removed legacy shim artifact: {legacy_path.name}")
    else:
        print("No changes needed. Derived sections already unsealed and lifecycle matches.")

if __name__ == "__main__":
    main()
