"""
twitterradar: The Python Twitter Radar Robot
============================================
"""
try:
    __ARM_SAPR_TOOLS_SETUP__
except NameError:
    __ARM_SAPR_TOOLS__ = False

if __ARM_SAPR_TOOLS__:
    import sys as _sys
    _sys.stderr.write("Running from arm_radar_tools source directory.\n")
    del _sys
else:
    import warnings as _warnings
    _warnings.simplefilter("always", DeprecationWarning)

    # import subpackages
    from . import plot
    from . import ingest
    from . import synthesize