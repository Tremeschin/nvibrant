"""This file is both a build script and hatchling hook"""

# /// script
# dependencies = [
#   "attrs~=25.4",
#   "hatchling~=1.29",
# ]
# ///

import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import attrs
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# ---------------------------------------------------------------------------- #

class Dirs:

    repository: Path = Path(__file__).parent
    """Repository root"""

    opengpu: Path = repository.joinpath("open-gpu")
    """Open GPU Kernel Modules submodule"""

    dist: Path = repository.joinpath("dist")
    """Distribution output directory"""

class Env:
    target:  str = "TARGET"
    workdir: str = "WORKDIR"

@attrs.define
class Target:
    wheel: str
    # cxx: str

# ---------------------------------------------------------------------------- #

class BuildHook(BuildHookInterface):
    def initialize(self, version: str, build: dict) -> None:
        try:
            self.target  = Target(**json.loads(os.environ[Env.target]))
            self.workdir = Path(os.environ[Env.workdir])
            self.buildir = self.workdir.joinpath("build")

        # Skip sdist install
        except KeyError:
            return None

        # Wheels are platform dependent
        build["tag"] = f"py3-none-{self.target.wheel}"
        build["pure_python"] = False

        # Configure the project
        subprocess.check_call((
            sys.executable, "-m", "mesonbuild.mesonmain",
            "setup", self.buildir,
            "--buildtype", "release",
            "--reconfigure", "--wipe",
        ), cwd=Dirs.repository)

        # Make binaries for all known driver version
        for driver in subprocess.check_output(
            ("git", "tag"), cwd=Dirs.opengpu
        ).decode().strip().splitlines():

            # Checkout driver version
            subprocess.check_call(
                ("git", "checkout", "-f", driver),
                cwd=Dirs.opengpu,
            )

            # Compile an executable
            subprocess.check_call((
                sys.executable, "-m", "ninja",
                "-C", self.buildir,
            ))

            # Find the compiled binary
            vendor = self.workdir/f"nvibrant-{driver}"
            binary = self.buildir.joinpath("nvibrant")
            binary.chmod(0o755)
            binary.rename(vendor)

            build["force_include"][str(vendor)] = \
                Path("nvibrant").joinpath("resources", vendor.name)

        # Revert back main branch
        subprocess.check_call(
            ("git", "checkout", "-f", "main"),
            cwd=Dirs.opengpu
        )

# --------------------------------------------------------------------------- #

TARGETS: tuple[Target] = (
    Target(
        wheel="manylinux_2_17_x86_64",
        # cxx="x86-64-linux-gnu-g++",
    ),
    # Target(
    #     wheel="manylinux_2_17_aarch64",
    #     cxx="aarch64-linux-gnu-g++",
    # ),
)

if __name__ == '__main__':

    # Intended operation
    subprocess.check_call(
        ("git", "config", "advice.detachedHead", "false"),
        cwd=Dirs.opengpu,
    )

    for target in TARGETS:
        with TemporaryDirectory(prefix="nvibrant-") as workdir:
            environ = os.environ.copy()
            environ[Env.target]  = json.dumps(attrs.asdict(target))
            environ[Env.workdir] = str(workdir)
            subprocess.check_call(
                args=("uv", "build", "--wheel", "-o", Dirs.dist),
                cwd=Dirs.repository,
                env=environ,
            )
