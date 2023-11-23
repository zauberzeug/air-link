# Air Admin

## Usage

### Local

1. Start On Air server with `./main.py`
2. Start Air Admin locally with `./main.py` (and let it point to the local On Air server "localhost")
3. Establish ssh connection to your local machine via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`

### Fly Preview

Note: Until On Air Server supports "ssh interconnect" login will only work if edge device is in the same region.

1. Start Air Admin locally with `python3 main.py` (and let it point to the On Air server (you can use `install.py` to make dependencies available)
2. Establish ssh connection to the machine where air admin is running via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@on-air.nicegui.io rodja@localhost`

You can also put the proxy jump into your `~/.ssh/config`:

```
Host air-preview-rodja
    HostName localhost
    User rodja
    ProxyJump zauberzeug/rodja@on-air.nicegui.io
```

## Deploy

Bring Air Admin to a new device by calling

```bash
./prime.py <target device> <on air token> --on-air-server=<the on air server>
```

It will put the air_admin code in the home dir of the user and start a system service.

You can re-run the installation locally on the device by calling

```bash
cd ~/air_admin
./install.py
```
