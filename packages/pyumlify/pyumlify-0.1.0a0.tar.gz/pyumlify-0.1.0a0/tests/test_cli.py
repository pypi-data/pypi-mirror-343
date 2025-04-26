def test_cli_generates_puml_files(tmp_path):
    """
    Run the CLI and check that .puml files are generated in the output directory.
    """

    import subprocess
    import sys
    import importlib.util

    # Ensure installation of the package
    assert importlib.util.find_spec("pyumlify") is not None, "pyumlify is not installed"
    
    out_dir = tmp_path / "uml_output"

    cmd = [
        sys.executable, "-m", "pyumlify",
         "--root", "tests/fixtures",
         "--output", str(out_dir),
         "--requirements", "tests/fixtures/requirements.txt"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Debug print if test fails
    if result.returncode != 0:
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

    assert result.returncode == 0, f"CLI failed:\n{result.stderr}"
    assert out_dir.exists(), "Output directory was not created"
    puml_files = list(out_dir.glob("*.puml"))
    assert puml_files, "No .puml files were generated"

    for file in puml_files:
        content = file.read_text()
        assert "@startuml" in content, f"{file.name} does not look like a valid PlantUML file"
