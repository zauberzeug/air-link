import sys
from pathlib import Path

import run


def starlette_templating() -> None:
    """Fixes a bug in starlette templating that prevents the app from running on Python < 3.8.2.

    See https://github.com/zauberzeug/air-admin/issues/1
    """
    file = Path('~/.local/lib/python3.8/site-packages/starlette/templating.py').expanduser()
    if file.read_text().find("'str',") >= 0:
        print('starlette templating already patched', flush=True)
        return

    if run.sudo(f'''sed -i "s/str,/'str',/g" {file}'''):
        print('patched starlette templating', flush=True)
    else:
        print('failed to patch starlette templating', flush=True)
        sys.exit(1)
