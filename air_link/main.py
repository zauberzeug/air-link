import argparse

from nicegui import app

from .install import install
from .run import run


def main() -> None:
    parser = argparse.ArgumentParser('Air Link',
                                     description='SSH access, diagnostics and administration for edge devices.')
    parser.add_argument('action', choices=['install', 'run', 'set-token'], help='action to perform', default='run')
    parser.add_argument('token', nargs='?',
                        help='On Air token for remote access (used with "install" or "set-token" actions)')
    parser.add_argument('--port', type=int, help='Port where the app should be launched (default: 4230)')
    args = parser.parse_args()

    if args.action == 'run':
        port = args.port or app.storage.general.get('air_link_port', 4230)
        run(port=port)

    if args.action == 'install':
        if args.token:
            app.storage.general['air_link_token'] = args.token
        if args.port:
            app.storage.general['air_link_port'] = args.port
        install()
        if args.token:
            print('Token is saved.')
        if args.port:
            print('Port is saved.')

    if args.action == 'set-token':
        if not args.token:
            print('Error: token argument is required')
            return
        app.storage.general['air_link_token'] = args.token
        print('Token is saved.')
