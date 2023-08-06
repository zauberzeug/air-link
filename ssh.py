import logging

import asyncssh
import socketio
from nicegui import background_tasks


class Server(asyncssh.SSHServer):
    def __init__(self, relay):
        self.relay = relay

    def connection_made(self, conn: asyncssh.SSHServerConnection):
        logging.info(f'SSH connection received from {conn.get_extra_info("peername")[0]}')
        self._conn = conn

    def begin_auth(self, username):
        ic(username)
        return False  # Allow anonymous access

    async def session_requested(self):
        ic()
        return Session(self.relay)


class Session(asyncssh.SSHServerSession):
    def __init__(self, relay: socketio.AsyncClient):
        self.relay = relay

    def connection_made(self, chan):
        ic()
        self._chan = chan

    def shell_requested(self):
        return True

    def exec_requested(self, command):
        ic(command)
        return False

    def data_received(self, data, datatype):
        background_tasks.create(self.relay.emit('ssh_data', {'data': data}))

    async def eof_received(self):
        return True
