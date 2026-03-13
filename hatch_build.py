import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import packaging.tags
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# ---------------------------------------------------------------------------- #

_workdir = TemporaryDirectory(prefix="nvibrant-")

class Dirs:

    repository: Path = Path(__file__).parent
    """Repository root"""

    opengpu: Path = repository.joinpath("open-gpu")
    """Open GPU Kernel Modules submodule"""

    dist: Path = repository.joinpath("dist")
    """Distribution output directory"""

    workdir: Path = Path(_workdir.name)
    """Temporary directory for building"""

    build: Path = workdir.joinpath("build")
    """Meson build directory"""

# ---------------------------------------------------------------------------- #

class BuildHook(BuildHookInterface):
    def initialize(self, version: str, build: dict) -> None:

        # Make wheels strictly for the host platform
        # https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/
        for tag in packaging.tags.sys_tags():

            # Skip generic linux not allowed in PyPI
            # https://github.com/pypa/packaging/issues/160
            if tag.platform.startswith("linux_"):
                continue
            if "local" in tag.platform:
                continue

            # Mark broader compatibility than host
            for arch in ("x86_64", "aarch64"):
                if arch not in tag.platform:
                    continue
                if "manylinux" in tag.platform:
                    build["tag"] = f"py3-none-manylinux_2_17_{arch}"
                elif "musllinux" in tag.platform:
                    build["tag"] = f"py3-none-musllinux_1_1_{arch}"
            break

        build["pure_python"] = False

        # Fixme: Ensure submodule

        # Configure the project
        subprocess.check_call((
            sys.executable, "-m", "mesonbuild.mesonmain",
            "setup", Dirs.build,
            "--buildtype", "release",
            "--reconfigure", "--wipe",
        ), cwd=Dirs.repository)

        # Intended operation
        subprocess.check_call(
            ("git", "config", "advice.detachedHead", "false"),
            cwd=Dirs.opengpu,
        )

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
                "-C", Dirs.build,
            ))

            # Find and vendor the binary for this version
            binary = Dirs.build.joinpath("nvibrant")
            target = Dirs.workdir/f"nvibrant-{driver}"
            target.write_bytes(binary.read_bytes())
            target.chmod(0o755)
            binary.unlink()

            # Include in the wheel
            build["force_include"][str(target)] = f"nvibrant/resources/{target.name}"

        # Revert back main branch
        subprocess.check_call(
            ("git", "checkout", "-f", "main"),
            cwd=Dirs.opengpu
        )
