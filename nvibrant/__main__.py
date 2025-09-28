import sys
from textwrap import dedent
from typing import NoReturn

from nvibrant import (
    __version__,
    get_best,
    get_driver,
    shell,
)


def main() -> NoReturn:
    (closest, nvibrant) = get_best()
    current = get_driver()

    # Ensure executable file and pass incoming argv
    call = shell("chmod", "+x", nvibrant, echo=False)
    call = shell(nvibrant, *sys.argv[1:], echo=False)

    if (call.returncode != 0):
        if (closest != current):
            print(dedent(f"""
                {'-'*80}

                Warn: nvibrant v{__version__} doesn't bundle exact binaries for your driver v{current},
                      the closest known previous version v{closest} was used but failed

                You can ignore this if the error is about usage and not ioctl. Note that there
                is some level of compatibility between driver versions, as the related code is
                mostly stable on nvidia's side. Chances are your driver is already supported,
                if there hasn't been a release in the last few days - check that here:

                • https://github.com/NVIDIA/open-gpu-kernel-modules/tags

                For Hybrid Systems (Integrated + Dedicated GPUs), please see the relevant readme
                section. Your best chances are on disabling the iGPU in the BIOS/UEFI altogether
                for nvidia to control the displays, expect much worse battery life with such!

                Otherwise, maybe there's a newer version available supporting your driver?

                • GitHub: https://github.com/Tremeschin/nvibrant
                • PyPI: https://pypi.org/project/nvibrant/
                • System update on your package manager\
            """))
        sys.exit(1)
    sys.exit(0)

if (__name__ == "__main__"):
    main()
