import pkgutil
import importlib
import sys

__all__ = []

for finder, name, ispkg in pkgutil.iter_modules(__path__):
    try:
        globals()[name] = importlib.import_module(f".{name}", package=__name__)
        __all__.append(name)
    except ImportError as e:
        print(f"[sphinxx] Failed to import submodule '{name}': {e}", file=sys.stderr)