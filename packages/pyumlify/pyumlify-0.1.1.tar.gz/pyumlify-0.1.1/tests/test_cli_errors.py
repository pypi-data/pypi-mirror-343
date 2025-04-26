import subprocess
import sys
from pathlib import Path

def test_cli_fails_with_invalid_root(tmp_path):
    """
    Test CLI behavior when given a non-existent root directory.
    """
    import importlib.util
    import re

    # Ensure installation of the package
    assert importlib.util.find_spec("pyumlify") is not None, "PyUMLify is not installed"
    
    invalid_path = tmp_path / "nonexistent"
    out_dir = tmp_path / "uml_out"

    result = subprocess.run(
        [sys.executable, "-m", "pyumlify", "--root", str(invalid_path), "--output", str(out_dir)],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0, "CLI should fail with non-existent root"
    assert "No such file or directory" in (result.stderr + result.stdout) or "not found" in (result.stderr + result.stdout), "Error message should indicate no such file or directory not found"
