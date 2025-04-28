
try:
    import PyQt6  # force addition of Qt6/bin to dll_directories
except ImportError:
    raise ImportError("PyQt6 must be installed in order to use PyQt6Ads.") from None

from ._ads import *
del PyQt6
            