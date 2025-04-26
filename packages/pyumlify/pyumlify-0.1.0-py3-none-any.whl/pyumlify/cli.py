import argparse
import os
from pathlib import Path
import sys
import shutil

from pyumlify.generate import (
    scan_project,
    generate_plantuml_files,
    get_known_external_modules
)

def main():
    """
    Entry point for the pyumlify CLI.
    """
    parser = argparse.ArgumentParser(description="Generate PlantUML diagrams for a Python project.")
    parser.add_argument("--root", type=str, default=".", help="Root directory of the Python project.")
    parser.add_argument("--output", type=str, default="./plantuml_output", help="Directory to store .puml files.")
    parser.add_argument("--requirements", type=str, default="requirements.txt", help="Path to requirements.txt file.")
    parser.add_argument("--include", type=str, nargs="*", default=[], help="Additional libraries to ignore (e.g. pandas)")
    parser.add_argument("--clear", action="store_true", help="Clear the output directory before generating")
    parser.add_argument("--force", action="store_true", default=False, help="Force overwrite of existing .puml files")

    args = parser.parse_args()

    root_path = Path(args.root).resolve()
    output_path = Path(args.output).resolve()

    if not os.path.isdir(root_path):
        print(f"❌ No such file or directory. '{root_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(root_path):
        print(f"❌ Error: No such file or directory. root directory '{root_path}' not found.", file=sys.stderr)
        exit(1)
    
    if not os.access(root_path, os.R_OK):
        print(f"❌ Cannot read from directory: {root_path}", file=sys.stderr)
        sys.exit(1)

    print("📐 PyUMLify is generating your UML diagrams...")

    # Optional: clear output directory
    if args.clear and os.path.exists(output_path):
        shutil.rmtree(output_path)

    # Load external libraries (std lib + requirements + extras)
    external_libs = get_known_external_modules(args.requirements)
    for lib in args.include:
        external_libs.add(lib.lower())

    # Run generation
    try:
        print("🔍 Scanning project...")
        project_data = scan_project(root_path)
        if not project_data:
            print("⚠️  No Python files found in the specified root directory.")
            exit(1)
        print(f"📦 Found {len(project_data)} modules.")
        print(args.force)
        print("📐 Generating PlantUML files...")
        generate_plantuml_files(project_data,
                                root_dir=root_path,
                                output_dir=output_path,
                                external_libs=external_libs,
                                force=args.force)
        print(f"✅ Done! Check the '{output_path}/' directory for the generated .puml files.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        exit(1)
