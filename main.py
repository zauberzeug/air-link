#!/usr/bin/env python3

import asyncio
import functools
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
        try:
            if ssh_chan is None:
                await create_ssh_connection(data['client_key'])
            ic(data['data'])
            ssh_chan.write(data['data'])
        except Exception as e:
            print('Error sending data to SSH:', e)

    async def create_ssh_connection(self, client_key):
        nonlocal ssh_chan
        ssh_conn = await asyncssh.connect('localhost', port=22, client_keys=[asyncssh.import_private_key(client_key)])
        ssh_chan = await ssh_conn.create_session(lambda: ssh.Session(self.relay), term_type='xterm')

# async def read_from_pty(self) -> None:
#     loop = asyncio.get_event_loop()
#     while True:
#         try:
#             data = await loop.run_in_executor(None, functools.partial(self.pty.read_nonblocking, 1024, timeout=1))
#             if data:
#                 await self.relay.emit('ssh_response', {'data': data})
#             else:
#                 break
#         except pexpect.TIMEOUT:
#             pass
#         except Exception as e:
#             print('Error reading from PTY:', e)


ui.run(favicon='🩺', storage_secret='secret', on_air='MD8wwLD9R3sy28nm')
