import asyncio
import logging
from typing import Any, Dict

from nicegui import background_tasks, core


def setup() -> None:
    incoming: Dict[str, asyncio.StreamWriter] = {}
    assert core.air is not None

    @core.air.relay.on('ssh_data')
    def from_socketio_to_tcp(data: Dict[str, Any]) -> None:
        if data['ssh_id'] in incoming:
            incoming[data['ssh_id']].write(data['payload'])
        else:
            logging.warning(f'received data for unknown ssh_id {data["ssh_id"]}')

    @core.air.relay.on('connect_ssh')
    async def connect_ssh(data: Dict[str, str]) -> None:
        ssh_id = data['ssh_id']
        try:
            reader, writer = await asyncio.open_connection('localhost', 22)
            incoming[ssh_id] = writer
            logging.info(f'created new ssh connection for {ssh_id}')
            background_tasks.create(outgoing(reader, ssh_id))
        except Exception as e:
            logging.exception(f'Unexpected error for ssh_id {ssh_id}: {e}')

    async def outgoing(reader, ssh_id):
        try:
            while not reader.at_eof():
                payload = await reader.read(1024)
                if payload:
                    await core.air.relay.emit('ssh_data', {'ssh_id': ssh_id, 'payload': payload})
        except ConnectionResetError:
            logging.exception(f'Connection reset by peer for ssh_id {ssh_id}, '
                              f'payload: {payload.decode() if payload else "empty"}')
        except Exception:
            logging.exception(f'Unexpected error for ssh_id {ssh_id}')
        finally:
            logging.info(f'ssh connection for {ssh_id} at eof or error')
            await disconnect_ssh({'ssh_id': ssh_id})

    @core.air.relay.on('disconnect_ssh')
    async def disconnect_ssh(data: Dict[str, str]) -> None:
        writer = incoming.pop(data['ssh_id'])
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        logging.info(f'ssh connection for {data["ssh_id"]} closed')
