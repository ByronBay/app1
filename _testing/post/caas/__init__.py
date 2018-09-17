__all__ = ["lib", "proc"]

from caas.lib import *
from caas.proc import *

import json

print("running __init__")


c_x11 = {}

try:
    with open('caas/colors/x11_rgb.json') as f:
        c_x11 = json.load(f)

except Exception:
    pass


c_xkcd = {}

try:
    with open("caas/colors/xkcd.json") as f:
        c_xkcd = json.load(f)

except Exception:
    pass
