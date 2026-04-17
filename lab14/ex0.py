"""
ex0.py
Task 0: Check whether SciPy, statsmodels, and matplotlib are installed.
"""

import importlib.util
import subprocess
import sys


def is_installed(package_name):
    """Return True if the named package can be imported."""
    return importlib.util.find_spec(package_name) is not None


def install_package(package_name):
    """Install a package using pip into the current Python environment."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


if __name__ == "__main__":
    packages = ["scipy", "statsmodels", "matplotlib"]
    missing = [package for package in packages if not is_installed(package)]

    if missing:
        print("Missing packages detected:")
        for package in missing:
            print(f"- {package}")
        print("Installing missing packages now...")
        for package in missing:
            install_package(package)
        print("Re-checking installed packages after installation...")

    report = {package: is_installed(package) for package in packages}
    print("Package installation report:")
    for package, installed in report.items():
        print(f"- {package}: {'Installed' if installed else 'Not installed'}")
    if not all(report.values()):
        print("\nSome packages could not be installed automatically. Install them manually using pip.")
