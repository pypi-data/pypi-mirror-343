import subprocess
import sys

def test_package_installation():
    """
    Test if the package can be installed in editable mode without errors.
    """
    print("Installing package in editable mode...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", ".", "--no-build-isolation"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("STDOUT:\\n", result.stdout)
        print("STDERR:\\n", result.stderr)

    assert result.returncode == 0, "Editable install failed"