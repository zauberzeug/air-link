import abc


class Capability(abc.ABC):

    def ensure(self):
        if not self.present():
            self.install()

    @abc.abstractmethod
    def present(self):
        pass

    @abc.abstractmethod
    def install(self):
        pass