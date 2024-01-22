import abc


class Capability(abc.ABC):

    def ensure(self) -> None:
        if not self.present():
            self.install()

    @abc.abstractmethod
    def present(self) -> bool:
        return False

    @abc.abstractmethod
    def install(self) -> None:
        pass
