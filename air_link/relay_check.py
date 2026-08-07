from __future__ import annotations

import asyncio
import logging

import httpx
from nicegui import app, core

CHECK_INTERVAL = 60.0  # seconds between checks
FAILURES_BEFORE_RECONNECT = 2


def setup() -> None:
    """Regularly verify that the On Air relay still serves this device; reconnect if it does not.

    The relay can drop a device while the socket.io client still believes it is connected
    (observed after network changes: the log shows "connected." without the following
    "on air at ..." line, or a loop of "packet queue is empty, aborting" that ends in silence).
    NiceGUI's reconnect timer only acts when the client knows it is disconnected,
    so the device would stay unreachable until the process is restarted.
    """
    consecutive_failures = 0

    async def relay_serves_this_device() -> bool | None:
        """Fetch the public status endpoint; ``None`` means the relay could not be reached at all."""
        assert core.air is not None
        if core.air.remote_url is None:
            return False  # the client connected, but the relay never announced the device URL
        try:
            async with httpx.AsyncClient() as client:
                # NOTE: probing "/status" rather than "/" keeps the relay from rendering the whole
                # main page in-process, which would block the event loop on Docker and disk calls
                response = await client.get(core.air.remote_url.rstrip('/') + '/status', timeout=15)
        except httpx.HTTPError:
            return None
        return response.status_code != 404

    async def check() -> None:
        nonlocal consecutive_failures
        if core.air is None or not core.air.relay.connected:
            consecutive_failures = 0  # NiceGUI reconnects on its own while the client knows it is disconnected
            return
        result = await relay_serves_this_device()
        if result is None:
            consecutive_failures = 0
            return  # the relay is unreachable (e.g. no internet), so reconnecting would not help
        consecutive_failures = 0 if result else consecutive_failures + 1
        if consecutive_failures < FAILURES_BEFORE_RECONNECT:
            return
        consecutive_failures = 0
        logging.warning('the On Air relay does not serve this device although the client seems connected; '
                        'disconnecting so NiceGUI reconnects')
        try:
            await asyncio.wait_for(core.air.disconnect(), timeout=10)
        except Exception:
            logging.exception('disconnecting from the On Air relay failed')

    app.timer(CHECK_INTERVAL, check)
