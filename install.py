#!/usr/bin/env python3

import getpass
import json
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

import run
from host_environment import HostEnvironment
from textfile import TextFile

if not run.sudo_password:
    run.sudo_password = getpass.getpass(prompt="Enter sudo password: ")

host = HostEnvironment.create()

run.pip('install -r requirements.txt')
ssh_keys = [key_file.read_text().strip() for key_file in Path('authorized_keys').glob('*.pub')]
TextFile(Path.home() / '.ssh' / 'authorized_keys').add_missing(ssh_keys)
TextFile('.env').update_lines(json.loads(Path('env_update.json').read_text()))

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