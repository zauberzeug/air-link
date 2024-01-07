import run

from . import Capability


class Buildx(Capability):

    def present(self):
        return run.sh('docker buildx version')

    def install(self):
        run.sh(
            'mkdir -p ~/.docker/cli-plugins/',
            'wget -O ~/.docker/cli-plugins/docker-buildx https://github.com/docker/buildx/releases/download/v0.12.0/buildx-v0.12.0.linux-arm64',
            'chmod a+x ~/.docker/cli-plugins/docker-buildx',
        )
