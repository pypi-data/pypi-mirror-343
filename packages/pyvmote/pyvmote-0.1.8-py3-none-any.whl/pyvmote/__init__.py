from .core import Pyvmote

__version__ = "0.1.8"

# Al importar pyvmote, devuelve una instancia automáticamente
_instance = Pyvmote()
import sys
sys.modules[__name__] = _instance