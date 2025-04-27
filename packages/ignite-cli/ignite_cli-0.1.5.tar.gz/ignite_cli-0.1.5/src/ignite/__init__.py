from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ignite-cli")  # 0.1.3
except PackageNotFoundError:
    __version__ = "0.0.0"
