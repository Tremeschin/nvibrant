import os
import subprocess
import sys
from textwrap import dedent

import nvibrant


def main():
    (closest, binary) = nvibrant.get_best()
    current = nvibrant.get_driver()

    # Files are force_include in hatchling instead of defined as shared_scripts,
    # so they are more easily accesible in resources dir (where this file is).
    # However, wheels (zips) doesn't support/might lose xattrs, ensure +x flag
    os.chmod(binary, 0o755)

    try:
        subprocess.check_call((binary, *sys.argv[1:]))
    except subprocess.CalledProcessError as call:
        if (closest != current):
            print(dedent(f"""
                {'-'*72}

                Warn: nvibrant doesn't bundle exact binaries for your v{current} driver;
                  the closest known, previous version v{closest} was used, but failed

                You can ignore this if the error above isn't related to ioctl calls.

                Note that there is some level of compatibility between major driver
                versions, as the related code is mostly stable on nvidia's side.

                Otherwise, maybe there is a new release supporting your driver?

                • GitHub: https://github.com/Tremeschin/nvibrant
                • PyPI: https://pypi.org/project/nvibrant/
                • System update on your package manager\
            """))
        sys.exit(call.returncode)

if (__name__ == "__main__"):
    main()
