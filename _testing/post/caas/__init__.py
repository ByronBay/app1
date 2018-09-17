__all__ = ["lib", "proc"]

from caas.lib import *
from caas.proc import *

import json

print("running __init__")

colors = {}


try:
    colors = {}
    with open('caas/colors/test.json') as f:
        colors = json.load(f)

    #colors["test"] = {}

    for color in colors:
        rgb_ = [color["r"], color["g"], color["b"]]
        for attribute, value in color.items():
            print(attribute)
            print(value)

except Exception:
    pass


try:
    c = {}
    with open('caas/colors/x11_rgb.json') as f:
        c = json.load(f)

    colors["x11"] = {}

except Exception:
    pass


try:
    c = {}
    with open("caas/colors/xkcd.json") as f:
        c = json.load(f)

    colors["xkcd"] = {}

except Exception:
    pass

print(colors)