#!/usr/bin/env python3

import re
from pathlib import Path

import run

nv_tegra_release_path = Path("/etc/nv_tegra_release")
if nv_tegra_release_path.is_file():
    l4t_version_string = nv_tegra_release_path.read_text().splitlines()[0]
    l4t_release_match = re.search(r'R(\d+)\s', l4t_version_string)
    l4t_revision_match = re.search(r'REVISION:\s([0-9.]+)', l4t_version_string)
    if l4t_release_match and l4t_revision_match:
        l4t_release = l4t_release_match.group(1)
        l4t_revision = l4t_revision_match.group(1)
        l4t_version = f"{l4t_release}.{l4t_revision}"
        if l4t_release == "32":
            if not run.sh('python3.8 --version'):
                print('installing Python 3.8')
                run.sh('sudo apt install software-properties-common -y')
                run.sh('sudo add-apt-repository ppa:deadsnakes/ppa -y')
                run.sh('sudo apt install python3.8 -y')
                run.sh('curl https://bootstrap.pypa.io/get-pip.py | python3.8')
            run.python_cmd = 'python3.8'

run.pip('install -r requirements.txt')
