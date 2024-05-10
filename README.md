# Air Admin

Air Admin is a standalone service to manage remote access to an edge device and to install user apps.

## Prerequisites

The edge device needs to run a Linux-based OS and have Python >=3.8 installed.

> [!NOTE]
> To install a recent Python version like 3.11, you can use [pyenv](https://github.com/pyenv/pyenv):
>
> ```bash
> # install dependencies
> sudo apt update
> sudo apt install build-essential libssl-dev zlib1g-dev \
> libbz2-dev libreadline-dev libsqlite3-dev curl \
> libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
>
> # install pyenv
> curl https://pyenv.run | bash
>
> # add pyenv to shell
> echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
> echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
> echo 'eval "$(pyenv init -)"' >> ~/.bashrc
>
> # source the bashrc
> source ~/.bashrc
>
> # install Python 3.11
> pyenv install 3.11
> pyenv global 3.11
> ```

## Setup

### 1. Deploy the Air Admin app to a new device

Run the following command on the developer machine to deploy the Air Admin app to an edge device.

```bash
./deploy.py <target device>
```

It will copy the Air Admin app into the home directory of the edge device and start it in a system service.
The app is accessible on port 8080 and can be reached via the IP address of the edge device.

> [!NOTE]
> To make the app accessible over an SSH tunnel, you can log into the edge device with the following command:
>
> ```bash
> ssh -L 8888:localhost:8080 w4
> ```
>
> The app will then be reachable at `localhost:8888` on the developer machine.

The system service will automatically start the app after a reboot.

> [!TIP]
> To display the logs of the Air Admin service, use the following command:
>
> ```bash
> journalctl -u air-admin -f
> ```
>
> The `-f` flag will follow the logs in real-time.

### 2. Access via NiceGUI On Air

To make the Air Admin app accessible via NiceGUI On Air, follow these three steps:

1.  Register a new device with a fixed region at <https://on-air.nicegui.io>.
2.  Enter the token in the top right corner of the Air Admin web interface.
3.  Restart the Air Admin service using the button next to the token.

Air Admin will be reachable through the URL provided by NiceGUI On Air, for example <https://on-air.nicegui.io/zauberzeug/rodja-admin>.

### 3. Manage SSH keys (optional)

To allow SSH access without a password, you can add SSH keys to the edge device using the Air Admin web interface.
Use the key icon in the top right corner to open the SSH key management.

## Usage

### Install User Apps

You can install user apps via the Air Admin web interface.
The web interface lists all available packages and provides a button to upload additional ZIP files.
The install button runs the `install.sh` script from the ZIP file and outputs the process in the web interface.

### SSH Login via NiceGUI On Air

Establish an SSH connection to the machine where Air Admin is running via proxy jump over the On Air server:

```bash
ssh -J <your_organization/<your_device_name>@on-air.nicegui.io root@localhost
```

Explanation:
The combination of organization and device name before the `@on-air.nicegui.io` tells the On Air server where to route the SSH login.
The last bit tells SSH with which user you want to log into the edge device
(which is `localhost` after Air Admin received the tunneled data from the On Air server).

> [!TIP]
> You can also put the proxy jump into your `~/.ssh/config` to establish a connection with the bash command `ssh my-device`:
>
> ```
> Host my-device
>     User root
>     HostName localhost
>     ProxyJump <your_organization/<your_device_name>@on-air.nicegui.io
> ```

## Development

### Design Decisions

- Assume an edge device with a Linux-based OS and Python >=3.8.
- Run side-by-side with user apps, because deploying/breaking a user app should not affect remote access.
- Provide SSH access to the edge device through the websocket tunnel from NiceGUI On Air.

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
