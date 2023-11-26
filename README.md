# Air Admin

Air Admin is a standalone service to administer an edge device.
The tool builds upon NiceGUI On Air which allows remote accessing an app running on some edge device.

## Usage

Note: Until On Air Server supports "ssh interconnect" login will only work if edge device is in the same region.

### 1. Deploy

Bring Air Admin to a new device by calling

```bash
./deploy.py <target device> --token <on air token> --server <the on air server>
```

It will put the air_admin code in the home dir of the user and start a system service.

You can re-run the installation locally on the device by calling

```bash
cd ~/air_admin
./install.py
```

Simply push latest code without modifying server or token:

```bash
./deploy.py <target device>
```

### 2. Remote Access

The Air Admin web interface will be reachable through the url provided by NiceGUI On Air.
For example: <https://on-air.nicegui.io/zauberzeug/rodja>

### 3. SSH Login

Establish ssh connection to the machine where air admin is running via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@on-air.nicegui.io rodja@localhost`

You can also put the proxy jump into your `~/.ssh/config`:

```
Host air-preview-rodja
    HostName localhost
    User rodja
    ProxyJump zauberzeug/rodja@on-air.nicegui.io
```

Explanation:
The organization and device id combination before the `@on-air.nicegui.io` tells the On Air server where to route the ssh login.
The last bit tells ssh with which user you want to log into the edge device
(which is `localhost` after Air Admin received the tunneled data from the On Air server).

## Development

## Design Decisions

- Provide ssh access to the edge device through the websocket tunnel from NiceGUI On Air.
- Run side-by-side with user apps, because deploying/braking a user app should not affect remote access.
- Focus on Linux based systems.
- Be compatible with Jetson Orin Nano (Ubuntu 18.04) which requires the code to work with Python 3.6+.
- Offer classes and functions to install and manage software (like `run.pip`, `TextFile('.env').update_lines({})`)

### Testing Local

1. Start On Air server with `./main.py`
2. Start Air Admin locally with `./main.py` (and let it point to the local On Air server "localhost")
3. Establish ssh connection to your local machine via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`
