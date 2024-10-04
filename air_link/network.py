import time

import aioping
from nicegui import app, ui

HISTORY_SIZE = 300


async def collect_data() -> None:
    try:
        latency = await aioping.ping('8.8.8.8', timeout=1)
    except TimeoutError:
        latency = None
    state = 'down' if latency is None else 'bad' if latency > 0.3 else 'good'
    events = app.storage.general.setdefault('network', [])
    if events and state == events[-1][1]:
        return

    timestamp = time.strftime(r'%Y-%m-%d %H:%M:%S')
    print('network:', state)
    events.append((timestamp, state))
    while len(events) > HISTORY_SIZE:
        events.pop(0)


def setup() -> None:
    ui.timer(1, collect_data)
