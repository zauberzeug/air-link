#!/usr/bin/env python3

import asyncio
from typing import Any, Dict

import asyncssh
import icecream
import nicegui.air
import nicegui.globals
from nicegui import app, background_tasks, ui

import ssh

icecream.install()
nicegui.air.RELAY_HOST = 'https://on-air-preview.fly.dev'
# nicegui.air.RELAY_HOST = 'http://localhost'

ui.label('Air Admin').classes('text-4xl')


@app.on_startup
async def startup():
    reader, writer = await asyncio.open_connection('localhost', 22)

    @nicegui.globals.air.relay.on('ssh_data')
    async def from_socketio_to_tcp(data: Dict[str, Any]) -> None:
        ic(data['data'])
        writer.write(data['data'])

    async def from_tcp_to_socketio() -> None:
        while not reader.at_eof():
            data = await reader.read(1024)
            ic(data)
            if data:
                await nicegui.globals.air.relay.emit('ssh_data', {'data': data})
        ic()

    @nicegui.globals.air.relay.on('connect_ssh')
    def connect_ssh() -> None:
        background_tasks.create(from_tcp_to_socketio())

ui.run(favicon='🩺', storage_secret='secret', on_air='MD8wwLD9R3sy28nm')
