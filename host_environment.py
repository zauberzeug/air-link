from __future__ import annotations

import re
import sys
from pathlib import Path

from packaging import version

import run


class HostEnvironment:

    def __init__(self) -> None:
        pass

    @staticmethod
    def create() -> HostEnvironment:
        if not Path('/etc/nv_tegra_release').exists():
            raise NotImplementedError('Host environment not recognized')
        return Jetson()


class Jetson(HostEnvironment):

    def __init__(self) -> None:
        super().__init__()
        print(f'Jetson {self.version} detected', flush=True)
        if self.version.major == 32:
            if not run.sh('python3.8 --version'):
                print('installing Python 3.8', flush=True)
                if not run.sudo(
                    'apt install software-properties-common -y',
                    'add-apt-repository ppa:deadsnakes/ppa -y',
                    'apt install python3.8 -y',
                    'curl https://bootstrap.pypa.io/get-pip.py | python3.8',
                ):
                    print('failed to install Python 3.8')
                    sys.exit(1)
            else:
                print('Python 3.8 already installed', flush=True)
        run.python_cmd = 'python3.8'

    @property
    def version(self) -> version.Version:
        l4t_version_string = Path('/etc/nv_tegra_release').read_text().splitlines()[0]
        l4t_release_match = re.search(r'R(\d+)\s', l4t_version_string)
        l4t_revision_match = re.search(r'REVISION:\s([0-9.]+)', l4t_version_string)
        assert l4t_release_match
        assert l4t_revision_match
        l4t_release = l4t_release_match.group(1)
        l4t_revision = l4t_revision_match.group(1)
        return version.parse(f'{l4t_release}.{l4t_revision}')
