#!/usr/bin/env python3
import getpass
import logging
import subprocess
from pathlib import Path

SERVICE_FILE = Path(__file__).parent / 'air-link.service'


def install() -> None:
    """Install Air Link as a service."""
    print('Installing Air Link as a service...')
    sudo_password = getpass.getpass(prompt='Enter sudo password: ')
    for cmd in [
        f'cp {SERVICE_FILE} /etc/systemd/system/air-link.service',
        'sed -i "s/USER/$USER/g" /etc/systemd/system/air-link.service',
        'systemctl daemon-reload',
        'systemctl enable air-link',
        'systemctl restart air-link',
        'sleep 5 # give service time to start',
        'systemctl status air-link || { journalctl -u air-link --no-pager -n 20; false; }',
    ]:
        sudo_cmd = f'sudo -S {cmd}'
        try:
            print(cmd)
            with subprocess.Popen(sudo_cmd,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  encoding='utf8') as process:
                stdout, stderr = process.communicate(input=sudo_password + '\n')
                if stdout:
                    print(stdout)
                if process.returncode != 0:
                    logging.error(f'Command failed with: {stderr}')
                    return
        except subprocess.CalledProcessError as e:
            logging.error(f'failed to run {sudo_cmd}: {e.output}')
            return
        except Exception as e:
            logging.exception(f'failed to run {sudo_cmd}: {e}')
            return
    print('\nAir Link service installed successfully.')
