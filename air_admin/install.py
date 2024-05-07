#!/usr/bin/env python3
import getpass

from utils import run

if not run.sudo_password:
    run.sudo_password = getpass.getpass(prompt='Enter sudo password: ')

run.pip('install -r requirements.txt')

run.sudo(
    'cp air_admin.service /etc/systemd/system/air_admin.service',
    'systemctl daemon-reload',
    'systemctl enable air_admin.service',
    'systemctl restart air_admin.service',
)
