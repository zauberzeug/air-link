#!/usr/bin/env python3
import argparse

from app import run
from install import install

parser = argparse.ArgumentParser('Air Link', description='SSH access, diagnostics and administration for edge devices.')
parser.add_argument('action', choices=['install', 'run'], help='action to perform', default='run')
args = parser.parse_args()

if args.action == 'run':
    run()

if args.action == 'install':
    install()
