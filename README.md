# Air Admin

Air Admin is a standalone service to administer an edge device.
The tool builds upon NiceGUI On Air which allows remote accessing an app running on some edge device.

## Usage

### 1. Register

Create a new device in the On Air web interface and note token and passphrase.
By convention the name should be `<device name>-admin`.
That way the descriptive device name without the postfix `-admin` is still free for the actual application using the On Air service.

NOTE: Make sure to set a fixed region for the device to ensure it does not accidentally move to a different region.

### 2. Deploy

Bring Air Admin to a new device by calling

```bash
./deploy.py <target device> [--token <on air token>] [--server <the on air server>]
```

It will put the Air Admin code in the home directory of the user and start a system service.
The token (and server) will be stored in `~/air_admin/.env` where it can be changed later.
If no token is provided in the deploy arguments the configuration in the `.env` will be kept.

You can re-run the installation locally on the device by calling

```bash
cd ~/air_admin
./install.py
```

To simply push the latest code without modifying server or token, call

```bash
./deploy.py <target device>
```

If you have SSH pub keys in the authorized_keys directory, they will be automatically installed on the target.

### 3. Remote Access

The Air Admin web interface will be reachable through the URL provided by NiceGUI On Air,
for example <https://on-air.nicegui.io/zauberzeug/rodja>.

### 4. SSH Login

Establish an SSH connection to the machine where Air Admin is running via proxy jump over the On Air server:

```bash
ssh -J <your_organization/<your_device_name>@on-air.nicegui.io root@localhost
```

Explanation:
The combination of organization and device name before the `@on-air.nicegui.io` tells the On Air server where to route the SSH login.
The last bit tells SSH with which user you want to log into the edge device
(which is `localhost` after Air Admin received the tunneled data from the On Air server).

You can also put the proxy jump into your `~/.ssh/config` to establish a connection with the bash command `ssh my-device`:

```
Host my-device
    User root
    HostName localhost
    ProxyJump <your_organization/<your_device_name>@on-air.nicegui.io
```

## Development

## Design Decisions

- Provide SSH access to the edge device through the websocket tunnel from NiceGUI On Air.
- Run side-by-side with user apps, because deploying/breaking a user app should not affect remote access.
- Focus on Linux-based systems.
- Be compatible with Jetson Orin Nano (Ubuntu 18.04), which requires parts of the code to work with Python 3.6+.
- Offer classes and functions to install and manage software (like `run.pip`, `TextFile('.env').update_lines({})`).

### Testing Locally

1. Start On Air server with `./main.py`.
2. Start Air Admin locally with `./main.py` (and let it point to the local On Air server "localhost").
3. Establish an SSH connection to your local machine via proxy jump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`.

### Formatting

We use [pre-commit](https://github.com/pre-commit/pre-commit) to make sure the coding style is enforced.
You first need to install pre-commit and the corresponding git commit hooks by running the following commands:

```bash
python3 -m pip install pre-commit
pre-commit install
```

After that you can make sure your code satisfies the coding style by running the following command:

```bash
pre-commit run --all-files
```

These checks will also run automatically before every commit.
