#!/usr/bin/env python3
import asyncio
import logging
import os
from typing import Any, Dict, Tuple

import icecream
import nicegui.air
from dotenv import load_dotenv
from nicegui import app, ui

logging.basicConfig(level=logging.INFO)
icecream.install()
load_dotenv('.env')

if os.environ.get('ON_AIR_SERVER'):
    nicegui.air.RELAY_HOST = os.environ.get('ON_AIR_SERVER')

ui.label('Air Admin').classes('text-4xl')
nicegui.air.RELAY_HOST = 'https://wasserbauer.zauberzeug.com/'


@app.on_startup
async def startup():
    incoming: Dict[str, asyncio.StreamWriter] = {}
    next_ssh_connection: Tuple[asyncio.StreamReader, asyncio.StreamWriter] = \
        await asyncio.open_connection('localhost', 22)

    @nicegui.air.instance.relay.on('ssh_data')
    def from_socketio_to_tcp(data: Dict[str, Any]) -> None:
        if data['ssh_id'] in incoming:
            incoming[data['ssh_id']].write(data['payload'])
        else:
            logging.warning(f'received data for unknown ssh_id {data["ssh_id"]}')

    @nicegui.air.instance.relay.on('connect_ssh')
    async def connect_ssh(data: Dict[str, str]) -> None:
        nonlocal next_ssh_connection
        reader, writer = next_ssh_connection
        ssh_id = data['ssh_id']
        incoming[ssh_id] = writer
        next_ssh_connection = await asyncio.open_connection('localhost', 22)
        logging.info(f'created new ssh connection for {ssh_id}')

        while not reader.at_eof():
            payload = await reader.read(1024)
            if payload:
                await nicegui.air.instance.relay.emit('ssh_data', {'ssh_id': ssh_id, 'payload': payload})

        logging.info(f'ssh connection for {ssh_id} at eof')
        await disconnect_ssh(data)

    @nicegui.air.instance.relay.on('disconnect_ssh')
    async def disconnect_ssh(data: Dict[str, str]) -> None:
        writer = incoming.pop(data['ssh_id'])
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        logging.info(f'ssh connection for {data["ssh_id"]} closed')

ui.run(favicon='⛑', storage_secret='secret', on_air=os.environ.get('ON_AIR_TOKEN'))
