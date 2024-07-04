#!/usr/bin/env python3
import getpass
import logging
import subprocess


def install() -> None:
    sudo_password = getpass.getpass(prompt='Enter sudo password: ')
    for cmd in [
        'cp air_link.service /etc/systemd/system/air_link.service',
        'sed -i "s/USER/$USER/g" /etc/systemd/system/air_link.service',
        'systemctl daemon-reload',
        'systemctl enable air_link.service',
        'systemctl restart air_link.service',
    ]:
        sudo_cmd = f'sudo -S {cmd}'
        try:
            with subprocess.Popen(sudo_cmd,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  encoding='utf8') as process:
                process.communicate(input=sudo_password + '\n')
                if process.wait() != 0:
                    return
        except subprocess.CalledProcessError as e:
            logging.error(f'failed to run {sudo_cmd}: {e.output}')
            return
        except Exception as e:
            logging.exception(f'failed to run {sudo_cmd}: {e}')
            return
