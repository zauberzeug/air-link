# Air Admin

## Usage

Note: currently only a freshly started On Air server and Air Admin can establish a ssh connection.
Allowing multiple sessions and reconnects is not yet implemented.

### Local

1. Start containerized On Air server with ssh branch with `docker compose up -d`
2. Start Air Admin locally with `python3 main.py` (and let it point to the local On Air server "localhost")
3. Establish ssh connection to your local machine via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`

### Fly

1. Deploy On Air server with ssh branch: `fly deploy`
2. make sure instance count is 1: `fly scale count 1`
3. Start Air Admin locally with `python3 main.py` (and let it point to the On Air server "on-air-preview.fly.dev")
4. Establish ssh connection to your local machine via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@168.220.85.116:2222 rodja@localhost`

Note: the ip address is allocated to point to the preview server;
the on-air-preview.fly.dev can not be used because the load balancer does not route arbitrary tcp traffic (or so I think).
