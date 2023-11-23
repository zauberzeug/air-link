#!/usr/bin/env python3

import getpass
import re
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import run

run.sudo_password = getpass.getpass(prompt="Enter sudo password: ")

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
                print('installing Python 3.8', flush=True)
                run.sudo(
                    'apt install software-properties-common -y',
                    'add-apt-repository ppa:deadsnakes/ppa -y',
                    'apt install python3.8 -y',
                    'curl https://bootstrap.pypa.io/get-pip.py | python3.8',
                )
            else:
                print('Python 3.8 already installed',flush=True)
            run.python_cmd = 'python3.8'

run.pip('install -r requirements.txt')
ssh_dir = Path.home() / '.ssh'
ssh_dir.mkdir(exist_ok=True)
authorized_keys_file = ssh_dir / 'authorized_keys'
with authorized_keys_file.open('r') as file:
    existing_keys = set(line.strip() for line in file)
with authorized_keys_file.open('a') as file:
    for key_file in Path('authorized_keys').glob('*.pub'):
        key = key_file.read_text().strip()
        if key and key not in existing_keys:
            file.write(f'{key}\n')

template = Environment(loader=FileSystemLoader('.')).get_template('air_admin.service.j2')
with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
    temp_file.write(template.render(python_cmd=run.python_cmd))
    temp_file.flush()
    run.sudo(
        f'cp {temp_file.name} /etc/systemd/system/air_admin.service',
        'systemctl daemon-reload',
        'systemctl enable air_admin.service',
        'systemctl restart air_admin.service',
    )