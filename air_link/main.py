import argparse

from .install import install
from .run import run


def main() -> None:
    parser = argparse.ArgumentParser(
        'Air Link', description='SSH access, diagnostics and administration for edge devices.')
    parser.add_argument('action', choices=['install', 'run'], help='action to perform', default='run')
    args = parser.parse_args()

    if args.action == 'run':
        run()

    if args.action == 'install':
        install()
