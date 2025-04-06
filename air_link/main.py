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
    args = parser.parse_args()

    if args.action == 'run':
        run()

    if args.action == 'install':
        if args.token:
            app.storage.general['air_link_token'] = args.token
        install()
        if args.token:
            print('Token is saved.')

    if args.action == 'set-token':
        if not args.token:
            print('Error: token argument is required')
            return
        app.storage.general['air_link_token'] = args.token
        print('Token is saved.')
