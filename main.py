#!/usr/bin/env python3

import asyncio
import logging
from typing import Any, Dict, Tuple

import icecream
import nicegui.air
import nicegui.globals
from nicegui import app, background_tasks, ui

logging.basicConfig(level=logging.INFO)

icecream.install()
# nicegui.air.RELAY_HOST = 'https://on-air-preview.fly.dev'
nicegui.air.RELAY_HOST = 'http://localhost'

ui.label('Air Admin').classes('text-4xl')


@app.on_startup
async def startup():
    incoming: Dict[str, asyncio.StreamWriter] = {}
    next_ssh_connection: Tuple[asyncio.StreamReader, asyncio.StreamWriter] = \
        await asyncio.open_connection('localhost', 22)

    @nicegui.globals.air.relay.on('ssh_data')
    async def from_socketio_to_tcp(data: Dict[str, Any]) -> None:
        if data['ssh_id'] in incoming:
            incoming[data['ssh_id']].write(data['payload'])
        else:
            logging.warning(f'received data for unknown ssh_id {data["ssh_id"]}')

    async def create_ssh_connection(ssh_id: str) -> None:
        nonlocal next_ssh_connection
        reader, writer = next_ssh_connection
        incoming[ssh_id] = writer
        next_ssh_connection = await asyncio.open_connection('localhost', 22)
        logging.info(f'created new ssh connection for {ssh_id}')

        while not reader.at_eof():
            data = await reader.read(1024)
            if data:
                await nicegui.globals.air.relay.emit('ssh_data', {'ssh_id': ssh_id, 'payload': data})

        logging.info(f'ssh connection for {ssh_id} closed')
        del incoming[ssh_id]

    @nicegui.globals.air.relay.on('connect_ssh')
    def connect_ssh(data: Dict[str, str]) -> None:
        background_tasks.create(create_ssh_connection(data['ssh_id']))

    @nicegui.globals.air.relay.on('disconnect_ssh')
    def disconnect_ssh(data: Dict[str, str]) -> None:
        if data['ssh_id'] in incoming:
            incoming[data['ssh_id']].close()
            logging.info(f'ssh connection for {data["ssh_id"]} closed')
            del incoming[data['ssh_id']]

ui.run(favicon='⛑', storage_secret='secret', on_air='MD8wwLD9R3sy28nm')
