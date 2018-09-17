__all__ = ["aux", "proc"]

from caas.lib import *
from caas.proc import *

import json
from pprint import pprint

print("running __init__")

c_x11 = {}

#with open('caas/colors/x11_rgb.json') as f:
#    c_x11 = json.load(f)

c_xkcd = {}

with open("caas/colors/xkcd.json") as f:
    c_xkcd = json.load(f)


pprint(c_xkcd)
