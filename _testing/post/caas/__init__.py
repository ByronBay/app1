__all__ = ["lib", "proc"]

from caas.lib import *
from caas.proc import *

import json
import numpy as np

print("running __init__")

colors = {}


try:
    colors = {}
    with open('caas/colors/test.json') as f:
        colors = json.load(f)

    n_colors = len(colors)

    rgbs = np.ndarray([0, 3])
    names = []
    comments = []

    for i, color in enumerate(colors):
        rgb_ = np.atleast_1d([color["r"], color["g"], color["b"]])

        rgbs = np.vstack([1, 2, 3], rgb_)
        names.append(color["literal name"])
        comments.append(color["comment"])

except Exception as e:
    print(e)

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
