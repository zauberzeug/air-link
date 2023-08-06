# Air Admin

## Usage

### Local

1. Start containerized On Air server with ssh branch with `docker compose up -d`
2. Start Air Admin locally with `python3 main.py`
3. Establish ssh connection to your local machine via ProxyJump over the On Air server: `ssh -J zauberzeug/rodja@localhost:2222 rodja@localhost`
