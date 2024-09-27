import importlib.metadata

try:
    __version__: str = importlib.metadata.version('air_link')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'dev'
