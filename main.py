#!/usr/bin/env python3

from typing import Any, Dict

import asyncssh
import icecream
import nicegui.air
import nicegui.globals
from nicegui import app, ui

import ssh

icecream.install()
# nicegui.air.RELAY_HOST = 'https://on-air-preview.fly.dev'
nicegui.air.RELAY_HOST = 'http://localhost'

ui.label('Air Admin').classes('text-4xl')


@app.on_startup
async def startup():
    ssh_chan = None

    @nicegui.globals.air.relay.on('ssh_data')
    async def on_ssh_data(data: Dict[str, Any]) -> None:
        nonlocal ssh_chan
        try:
            if ssh_chan is None:
                ssh_chan = await create_ssh_connection(data['client_key'])
            ssh_chan.write(data['data'])
        except Exception as e:
            print('Error sending data to SSH:', e)

    async def create_ssh_connection(client_key):
        ssh_conn = await asyncssh.connect('localhost', port=22, client_keys=[asyncssh.import_private_key(client_key)])
        return await ssh_conn.create_session(lambda: ssh.Session(nicegui.globals.air.relay), term_type='xterm')


ui.run(favicon='🩺', storage_secret='secret', on_air='MD8wwLD9R3sy28nm')
