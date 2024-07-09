# Air Link

Air Link is a standalone service to manage remote access to an edge device and to install user apps.

[![PyPI](https://img.shields.io/pypi/v/air-link?color=dark-green)](https://pypi.org/project/air-link/)
[![PyPI downloads](https://img.shields.io/pypi/dm/air-link?color=dark-green)](https://pypi.org/project/air-link/)
[![GitHub license](https://img.shields.io/github/license/zauberzeug/air-link?color=orange)](https://github.com/zauberzeug/air-link/blob/main/LICENSE)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/zauberzeug/air-link)](https://github.com/zauberzeug/air-link/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/zauberzeug/air-link?color=blue)](https://github.com/zauberzeug/air-link/issues)
[![GitHub forks](https://img.shields.io/github/forks/zauberzeug/air-link)](https://github.com/zauberzeug/air-link/network)
[![GitHub stars](https://img.shields.io/github/stars/zauberzeug/air-link)](https://github.com/zauberzeug/air-link/stargazers)

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
> # add pyenv to login shell .profile, maybe also .bashrc, .zshrc, etc. depending on your shell
> # see https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv
> echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
> echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
> echo 'eval "$(pyenv init -)"' >> ~/.profile
>
> # source the bashrc
> source ~/.bashrc
>
> # install Python 3.11
> pyenv install 3.11
> pyenv global 3.11
> ```

## Setup

### 1. Install the Air Link app on an edge device

Air link can be installed using pip.
To run the app automatically after a reboot, you can install it as a system service using its `install` command.

```bash
pip install air-link
air-link install
```

The app is accessible on port 8080 and can be reached via the IP address of the edge device.

> [!NOTE]
> To make the app accessible over an SSH tunnel, you can log into the edge device with the following command:
>
> ```bash
> ssh -L 8888:localhost:8080 <target device>
> ```
>
> The app will then be reachable at `localhost:8888` on the developer machine.

> [!TIP]
> To display the logs of the Air Link service, use the following command:
>
> ```bash
> journalctl -u air_link -f
> ```
>
> The `-f` flag will follow the logs in real-time.

### 2. Access via NiceGUI On Air

To make the Air Link app accessible via NiceGUI On Air, follow these three steps:

1.  Register a new device with a fixed region at <https://on-air.nicegui.io>.
2.  Enter the token in the top right corner of the Air Link web interface.
3.  Restart the Air Link service using the button next to the token.

Air Link will be reachable through the URL provided by NiceGUI On Air, for example <https://europe.on-air.io/zauberzeug/rodja-air-link>.
We strongly suggest to set a fixed region for the device at <https://on-air.nicegui.io> to keep the URL stable.

### 3. Manage SSH keys (optional)

To allow SSH access without a password, you can add SSH keys to the edge device using the Air Link web interface.
Use the key icon in the top right corner to open the SSH key management.

## Usage

### Install User Apps

You can install user apps via the Air Link web interface.
The web interface lists all available packages and provides a button to upload additional ZIP files.
The install button runs the `install.sh` script from the ZIP file and outputs the process in the web interface.

### SSH Login via NiceGUI On Air

Establish an SSH connection to the machine where Air Link is running via proxy jump over the On Air server:

```bash
ssh -J <your_organization>/<your_device_name>@<your_region>.on-air.io <username_on_device>@localhost
```

Explanation:
The combination of organization and device name before the `@<region>.on-air.io` tells the On Air server where to route the SSH login.
The last bit tells SSH with which user you want to log into the edge device
(which is `localhost` after Air Link received the tunneled data from the On Air server).

> [!TIP]
> You can also put the proxy jump into your `~/.ssh/config` to establish a connection with the bash command `ssh my-device`:
>
> ```
> Host my-device
>     User <your_username>
>     HostName localhost
>     ProxyJump <your_organization>/<your_device_name>@<your_region>.on-air.io
> ```
>
> It may also be beneficial to add the following configuration to the host entry:
>
> ```
>     StrictHostKeyChecking no
>     UserKnownHostsFile /dev/null
>     ServerAliveInterval 30
>     ForwardAgent yes
>     SetEnv GIT_AUTHOR_NAME="Your Name" EMAIL="your.email@example.com"
> ```

## Development

### Design Decisions

- Assume an edge device with a Linux-based OS and Python >=3.8.
- Run side-by-side with user apps, because deploying/breaking a user app should not affect remote access.
- Provide SSH access to the edge device through the websocket tunnel from NiceGUI On Air.

### Testing Locally

1. Start On Air server with `./main.py`.
2. Start Air Link locally with `./main.py` (and let it point to the local On Air server "localhost").
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

### Deployment

To deploy a new version of Air Link, add a new tag with the format `vX.Y.Z` and push it to the repository.
The CI pipeline will then build the new version, upload it to PyPI, and create a new draft release on GitHub.
