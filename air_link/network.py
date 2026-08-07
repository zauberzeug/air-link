import asyncio
import time

import aioping
from nicegui import app, helpers

HISTORY_SIZE = 300
lock = asyncio.Lock()


async def collect_data() -> None:
    async with lock:
        error: OSError | None = None
        try:
            latency = await aioping.ping('8.8.8.8', timeout=2)
        except PermissionError:
            latency = None  # the network is recorded as down
            helpers.warn_once('Could not send an ICMP echo request, so the network is recorded as down. '
                              'Re-run "air-link install" to grant the service the CAP_NET_RAW capability.')
        except OSError as e:
            latency = None  # e.g. a timeout or an unreachable network
            error = e
        state = 'down' if latency is None else 'bad' if latency > 1.0 else 'good'
        events = app.storage.general.setdefault('network', [])
        if events and state == events[-1][1]:
            return

        timestamp = time.strftime(r'%Y-%m-%d %H:%M:%S')
        print('network:', state if error is None else f'{state} ({error})', flush=True)
        events.append((timestamp, state))
        while len(events) > HISTORY_SIZE:
            events.pop(0)


def setup() -> None:
    app.timer(1, collect_data)
