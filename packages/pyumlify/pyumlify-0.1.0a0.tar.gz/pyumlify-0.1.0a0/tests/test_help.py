import subprocess
import sys

def test_cli_help_message():
    """
    Ensure that the --help message works without error.
    """
    import importlib.util

    # Ensure installation of the package
    assert importlib.util.find_spec("pyumlify") is not None, "pyumlify is not installed"
    
    # Run the CLI with --help
    result = subprocess.run(
        [sys.executable, "-m", "pyumlify", "--help"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "--help should not fail"
    assert "Generate PlantUML diagrams" in result.stdout
    assert "--root" in result.stdout
    assert "--output" in result.stdout
