import time

import aioping
from nicegui import app, ui


async def collect_data():
    try:
        latency = await aioping.ping('8.8.8.8', timeout=1)
        latency_ms = round(latency * 1000, 2)
    except TimeoutError:
        latency_ms = None
    storage = app.storage.general
    storage.setdefault('network', [])
    if latency_ms is None:
        state = 'network_down'
    elif latency_ms > 100:
        state = 'network_bad'
    else:
        state = 'network_good'
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    events = storage.get('network')
    if events and state != events[-1][1]:
        print(timestamp, state)
        storage['network'].append((timestamp, state))
        if len(storage['network']) > 300:
            storage['network'].pop(0)


def setup():
    ui.timer(1, collect_data)
