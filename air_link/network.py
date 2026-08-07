import asyncio
import logging
import time

import aioping
from nicegui import app
from nicegui.timer import Timer

HISTORY_SIZE = 300
lock = asyncio.Lock()


async def collect_data(timer: Timer) -> None:
    async with lock:
        try:
            latency = await aioping.ping('8.8.8.8', timeout=2)
        except PermissionError:
            timer.deactivate()
            logging.warning('Could not open an ICMP socket, so the network history stays empty. '
                            'Re-run "air-link install" to grant the service the CAP_NET_RAW capability.')
            return
        except OSError:
            latency = None  # e.g. a timeout or an unreachable network
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
    timer: Timer = app.timer(1, lambda: collect_data(timer))
