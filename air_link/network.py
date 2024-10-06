import asyncio
import time

import aioping
from nicegui import app, ui

HISTORY_SIZE = 300
lock = asyncio.Lock()


async def collect_data() -> None:
    async with lock:
        try:
            latency = await aioping.ping('8.8.8.8', timeout=2)
        except TimeoutError:
            latency = None
        state = 'down' if latency is None else 'bad' if latency > 1.0 else 'good'
        events = app.storage.general.setdefault('network', [])
        if events and state == events[-1][1]:
            return

        timestamp = time.strftime(r'%Y-%m-%d %H:%M:%S')
        print('network:', state, flush=True)
        events.append((timestamp, state))
        while len(events) > HISTORY_SIZE:
            events.pop(0)


def setup() -> None:
    ui.timer(1, collect_data)
