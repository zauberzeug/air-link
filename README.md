# Air Admin

Air Admin is a standalone service to administer an edge device.
The tool builds upon NiceGUI On Air which allows remote accessing an app running on some edge device.

## Usage

Note: Until On Air Server supports "SSH interconnect", login will only work if the edge device is in the same region.

### 1. Deploy

Bring Air Admin to a new device by calling

```bash
./deploy.py <target device> --token <on air token> [--server <the on air server>]
```

It will put the Air Admin code in the home directory of the user and start a system service.

You can re-run the installation locally on the device by calling

```bash
cd ~/air_admin
./install.py
```

To simply push the latest code without modifying server or token, call

```bash
./deploy.py <target device>
```

If you have ssh pub keys in the authorized_keys directory they will be automatically installed on the target.

### 2. Remote Access

The Air Admin web interface will be reachable through the URL provided by NiceGUI On Air,
for example <https://on-air.nicegui.io/zauberzeug/rodja>.

### 3. SSH Login

Establish an SSH connection to the machine where Air Admin is running via proxy jump over the On Air server:

```bash
ssh -J zauberzeug/rodja@on-air.nicegui.io rodja@localhost
```

You can also put the proxy jump into your `~/.ssh/config`:

```
Host air-preview-rodja
    HostName localhost
    User rodja
    ProxyJump zauberzeug/rodja@on-air.nicegui.io
```

Explanation:
The combination of organization and device ID before the `@on-air.nicegui.io` tells the On Air server where to route the SSH login.
The last bit tells SSH with which user you want to log into the edge device
(which is `localhost` after Air Admin received the tunneled data from the On Air server).

## Development

## Design Decisions

- Provide SSH access to the edge device through the websocket tunnel from NiceGUI On Air.
- Run side-by-side with user apps, because deploying/braking a user app should not affect remote access.
- Focus on Linux-based systems.
- Be compatible with Jetson Orin Nano (Ubuntu 18.04), which requires parts of the code to work with Python 3.6+.
- Offer classes and functions to install and manage software (like `run.pip`, `TextFile('.env').update_lines({})`).

### Testing Locally

1. Start On Air server with `./main.py`.
2. Start Air Admin locally with `./main.py` (and let it point to the local On Air server "localhost").
3. Establish an SSH connection to your local machine via proxy jump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`.
