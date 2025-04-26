

![PyUMLify Banner](https://raw.githubusercontent.com/guipatriota/pyumlify/main/assets/banner.png)

# PyUMLify

**Automatically generate UML class and package diagrams from your Python project using PlantUML.**

**PyUMLify** is a lightweight Python tool that scans your project's source code and automatically generates PlantUML class and package diagrams. It's designed to improve documentation and architecture visibility in any Python-based project — whether it's a microservice, CLI, library, or monolith.

---

## ✨ What is it?

**PyUMLify** scans your Python project to identify classes, methods, and their relationships, and then generates `.puml` files ready to be rendered with [PlantUML](https://plantuml.com/).

## 🚀 Installation

```bash
pip install pyumlify
```

Or, if you're developing or testing locally:

```bash
git clone https://github.com/guipatriota/pyumlify.git
cd pyumlify
pip install -e .
```

## 🛠️ Usage

```bash
pyumlify --root . --output plantuml_output
```

Optional flags:

- `--requirements`: path to your `requirements.txt` (default is `requirements.txt`)
- `--include`: extra external libraries to ignore (e.g. `--include pandas numpy`)
- `--clear`: remove the output directory before generating
- `--force`: overwrite `.puml` files even if they already exist

Example:

```bash
pyumlify --root src/ --output uml/ --requirements requirements.txt --include pandas numpy --force
```

## 📦 Output

- One `.puml` file per package/module
- A `packages.puml` showing the relationships between modules

You can visualize the diagrams using:

- [PlantUML](https://plantuml.com/)
- [VSCode Plugin](https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml)
- Any tool that supports `.puml` rendering

## 📌 Features

- 📂 Supports large Python projects with nested folders
- 📚 Detects class dependencies and method return types
- 🧠 Ignores standard libraries and known third-party packages
- 💡 Highlighted themes and class formatting included

## 🧪 Testing

Run all tests using:

```bash
pytest
```

## 📄 License

GPL3.0 License. See `LICENSE` file for details.

---

Made with ❤️ by [Guilherme Ditzel Patriota](https://github.com/guipatriota)