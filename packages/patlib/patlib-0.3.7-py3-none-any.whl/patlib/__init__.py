"""A small, personal, snippet library."""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore

# https://github.com/python-poetry/poetry/pull/2366#issuecomment-652418094
__version__ = importlib_metadata.version(__name__)
