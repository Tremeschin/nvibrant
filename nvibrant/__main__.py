import os
import subprocess
import sys

import nvibrant


def main() -> None:
    (version, binary) = nvibrant.get_best()
    driver = nvibrant.get_driver()

    # Files are force_include in hatchling instead of defined as shared_scripts,
    # so they are more easily accesible in resources dir (where this file is).
    # However, wheels (zips) doesn't support/might lose xattrs, ensure +x flag
    try:
        os.chmod(binary, 0o755)
    except OSError:
        pass

    try:
        subprocess.check_call((binary, *sys.argv[1:]))
    except subprocess.CalledProcessError as call:
        if (version != driver):
            print(f"""
{'-'*72}

Warn: nvibrant doesn't bundle exact binaries for your driver v{driver},
    the closest known, previous version v{version} was used, but failed

You can ignore this if the error above isn't related to ioctl calls.

Note that there is some level of compatibility between major driver
versions, as the related code is mostly stable on nvidia's side.

Otherwise, maybe there is a new release supporting your driver?

• GitHub: https://github.com/Tremeschin/nvibrant
• PyPI: https://pypi.org/project/nvibrant/
• System update on your package manager\
            """)

        sys.exit(call.returncode)

if (__name__ == "__main__"):
    main()
