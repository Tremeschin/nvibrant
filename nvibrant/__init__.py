import os
import sys
from pathlib import Path

from packaging.version import Version

resources: Path = Path(__file__).parent.joinpath("resources")
"""Path to the package resources directory"""

def get_driver() -> Version:
    """Current nvidia driver version"""
    variable: str = "NVIDIA_DRIVER_VERSION"

    # Safety fallback or override with environment variable
    if (force := os.getenv(variable)):
        return Version(force)

    # Seems to be a common and stable path to get the information
    if (file := Path("/sys/module/nvidia/version")).exists():
        return Version(file.read_text("utf-8").strip())

    print("Could not find the current driver version in /sys/module/nvidia/version")
    print(f"• Run with '{variable}=x.y.z nvibrant' to set or force it")
    sys.exit(1)

def get_versions() -> dict[Version, Path]:
    """Compiled binary versions to their paths"""
    versions = dict()

    # eg "nvibrant-515.43.04"
    for file in resources.glob("*"):
        version = Version(file.stem.split("-")[1])
        versions[version] = file

    return versions

def get_best() -> tuple[Version, Path]:
    """
    Get the highest compiled version that is (or should be) compatible with the
    current driver. Mismatches have a good chance of working even across major
    releases, this makes it so that patch bumps don't need a new build every
    time. You can't win if you don't play otherwise, right?
    """
    options = get_versions()
    current = get_driver()
    optimal = max(x for x in options if x <= current)
    return (optimal, options[optimal])
