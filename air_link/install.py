#!/usr/bin/env python3
import getpass

from utils import run

if not run.sudo_password:
    run.sudo_password = getpass.getpass(prompt='Enter sudo password: ')

run.pip('install -r requirements.txt')

run.sudo(
    'cp air_link.service /etc/systemd/system/air_link.service',
    'sed -i "s/USER/$USER/g" /etc/systemd/system/air_link.service',
    'systemctl daemon-reload',
    'systemctl enable air_link.service',
    'systemctl restart air_link.service',
)
