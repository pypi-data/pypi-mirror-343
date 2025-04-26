__all__ = [
    "scan_project", "generate_plantuml_files", "get_known_external_modules"
]

import os
import ast
from pathlib import Path
import importlib.metadata
from collections import defaultdict
from stdlib_list import stdlib_list

# Helpers
def get_args(function_node):
    return [arg.arg for arg in function_node.args.args if arg.arg != 'self']

def get_return_annotation(node):
    try:
        return ast.unparse(node.returns) if node.returns else None
    except Exception:
        return None

def get_top_level_imports():
    import_names = set()
    for dist in importlib.metadata.distributions():
        fallback = dist.metadata["Name"].lower().replace("-", "_")
        try:
            top_level_txt = dist.read_text('top_level.txt')
            if top_level_txt:
                import_names.update(name.strip().lower().replace("-", "_") for name in top_level_txt.splitlines())
            else:
                import_names.add(fallback)
        except Exception:
            import_names.add(fallback)
    return import_names

def load_external_libraries_from_requirements(filepath="requirements.txt"):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, "r", encoding="utf-8") as f:
        return {line.strip().split("==")[0].lower().replace("-", "_") for line in f if line.strip() and not line.startswith("#")}

def get_known_external_modules(requirements_path):
    stdlib_modules = {mod.lower().replace("-", "_") for mod in stdlib_list()}
    req_modules = load_external_libraries_from_requirements(requirements_path)
    top_level_imports = get_top_level_imports()
    problematic_modules = {"PyPDF2"}
    return stdlib_modules.union(req_modules).union(top_level_imports).union(problematic_modules)

def extract_structure(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        print(f"⚠️ Skipping file due to syntax error: {filepath} ({e})")
        return None
    except UnicodeDecodeError:
        return None

    result = {
        "file": filepath,
        "classes": [],
        "imports": set()
    }

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                pkg = alias.name.split(".")[0]
                result["imports"].add(pkg)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                pkg = node.module.split(".")[0]
                result["imports"].add(pkg)

        elif isinstance(node, ast.ClassDef):
            if node.name == "Main" and not filepath.endswith("main.py") and not filepath.endswith("app.py"):
                continue
            class_info = {
                "name": node.name,
                "line": node.lineno,
                "methods": [],
                "attributes": []
            }
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    class_info["methods"].append({
                        "name": item.name,
                        "line": item.lineno,
                        "args": get_args(item),
                        "returns": get_return_annotation(item)
                    })
                elif isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            class_info["attributes"].append({
                                "name": target.id,
                                "line": item.lineno
                            })
            result["classes"].append(class_info)

    result["imports"] = list(result["imports"])
    return result

def scan_project(root):
    results = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".py"):
                full_path = os.path.join(dirpath, filename)
                structure = extract_structure(full_path)
                if structure:
                    results.append(structure)
    return results

def extract_package(filepath, root_dir):
    rel_path = os.path.relpath(filepath, root_dir)
    parts = rel_path.split(os.sep)
    return os.path.splitext(parts[0])[0] if len(parts) == 1 else parts[0]

def detect_dependencies(cls, all_class_names):
    deps = set()
    for method in cls.get("methods", []):
        for arg in method.get("args", []):
            for name in all_class_names:
                if name.lower() in arg.lower() and name != cls["name"]:
                    deps.add(name)
        ret = method.get("returns")
        if ret and ret in all_class_names and ret != cls["name"]:
            deps.add(ret)
    return deps

def clean_dependencies(dependencies, external_libs):
    cleaned = {}
    for from_pkg, to_pkgs in dependencies.items():
        if from_pkg in external_libs:
            continue
        cleaned_to_pkgs = {pkg for pkg in to_pkgs if pkg not in external_libs}
        if cleaned_to_pkgs:
            cleaned[from_pkg] = cleaned_to_pkgs
    return cleaned

def clean_package_classes(package_classes, external_libs):
    cleaned = {}
    for pkg, classes in package_classes.items():
        if pkg in external_libs:
            continue
        cleaned[pkg] = classes
    return cleaned

def generate_plantuml_files(project_data, root_dir=".", output_dir="./plantuml_output", external_libs=None, force=False):
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        print(f"❌ Permission denied to create or write to output directory: {output_dir}")
        exit(1)
    package_classes = defaultdict(list)
    class_to_package = {}
    all_class_names = set()
    import_dependencies = defaultdict(set)

    for entry in project_data:
        package = extract_package(entry["file"], root_dir)
        for cls in entry.get("classes", []):
            class_to_package[cls["name"]] = package
            package_classes[package].append(cls)
            all_class_names.add(cls["name"])
        for imp in entry.get("imports", []):
            import_dependencies[package].add(imp)

    for pkg, imports in import_dependencies.items():
        for imp in imports:
            if imp not in package_classes:
                package_classes[imp] = []

    dependencies = defaultdict(set)
    for pkg, classes in package_classes.items():
        for cls in classes:
            deps = detect_dependencies(cls, all_class_names)
            for dep in deps:
                dep_pkg = class_to_package.get(dep)
                if dep_pkg and dep_pkg != pkg:
                    dependencies[pkg].add(dep_pkg)
        for imp in import_dependencies[pkg]:
            if imp != pkg:
                dependencies[pkg].add(imp)

    # Clean dependencies
    dependencies = clean_dependencies(dependencies, external_libs)
   
    # Clean package_classes
    package_classes = clean_package_classes(package_classes, external_libs)
    
    for package, classes in package_classes.items():
        if not classes and external_libs and package in external_libs:
            continue
        if os.path.exists(os.path.join(output_dir, f"{package}.puml")) and not force:
            print(f"⚠️  File {package}.puml already exists. Use --force to overwrite.")
            continue
        with open(os.path.join(output_dir, f"{package}.puml"), "w", encoding="utf-8") as f:
            f.write(f"@startuml {package}\n")
            f.write("!include https://raw.githubusercontent.com/guipatriota/dracula-plantuml-theme/v1.0.0/theme.puml\n")
            f.write("skinparam classAttributeIconSize 0\n\n")
            for cls in classes:
                f.write(f"class {cls['name']} {{\n")
                for m in cls["methods"]:
                    if m["name"] == "__init__":
                        continue
                    args = ", ".join(m.get("args", []))
                    ret = f": {m['returns']}" if m['returns'] else ""
                    f.write(f"  +{m['name']}({args}){ret}\n")
                for a in cls["attributes"]:
                    f.write(f"  -{a['name']}\n")
                f.write("}\n\n")
            f.write("@enduml\n")

        print(f"✅ Created {len(classes)} classes in '{package}.puml'")

    if os.path.exists(os.path.join(output_dir, "packages.puml")) and not force:
        print(f"⚠️  File packages.puml already exists. Use --force to overwrite.")
        return
    with open(os.path.join(output_dir, "packages.puml"), "w", encoding="utf-8") as f:
        f.write("@startuml packages\n")
        f.write("!include https://raw.githubusercontent.com/guipatriota/dracula-plantuml-theme/v1.0.0/theme.puml\n")
        f.write("skinparam packageStyle rect\n\n")
        for pkg in package_classes:
            if external_libs and pkg in external_libs:
                continue
            f.write(f'package "{pkg}" as {pkg} {{}}\n')
        for from_pkg, to_pkgs in dependencies.items():
            if external_libs and from_pkg in external_libs:
                continue
            for to_pkg in to_pkgs:
                if external_libs and to_pkg in external_libs:
                    continue
                f.write(f"{from_pkg} --> {to_pkg}\n")
        f.write("@enduml\n")
        print(f"✅ Created {len(package_classes)} packages in 'packages.puml'")
