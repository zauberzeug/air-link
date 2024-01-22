import run

from . import Capability

URL = 'https://github.com/docker/buildx/releases/download/v0.12.0/buildx-v0.12.0.linux-arm64'


class Buildx(Capability):

    def present(self) -> bool:
        return run.sh('docker buildx version')

    def install(self) -> None:
        run.sh(
            'mkdir -p ~/.docker/cli-plugins/',
            f'wget -O ~/.docker/cli-plugins/docker-buildx {URL}',
            'chmod a+x ~/.docker/cli-plugins/docker-buildx',
        )
