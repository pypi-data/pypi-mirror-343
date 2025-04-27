from ._version import __version__
from .global_context import Global, GlobalRegistrationError
from .auto_init import register_global_module, auto_initialize_globals

__all__ = ["Global", "GlobalRegistrationError", "register_global_module", "auto_initialize_globals"]
