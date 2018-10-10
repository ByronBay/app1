import json
import numpy as np
import pathlib

color_definitions = {}

storage_root = pathlib.PurePath('.',"data")

def import_color_definitions(name, pfnColorDefinition, colors_collected):

    try:

        colors_from_file = {}
        with open(pfnColorDefinition) as f:
            colors_from_file = json.load(f)

        n_colors = len(colors_from_file)

        rgbs = np.array([])
        names = []
        comments = []

        for single_color in colors_from_file:
            rgb_ = np.atleast_1d(
                [single_color["r"], single_color["g"], single_color["b"]])

            rgbs = np.append(rgbs, rgb_)
            names.append(single_color["literal name"])
            comments.append(single_color["comment"])

        rgbs = np.reshape(rgbs, (n_colors, -1))
    except Exception as e:
        print(e)

    colors_collected[name] = {"rgbs": rgbs,
                              "names": names, "comments": comments}


# import_color_definitions("test", "caas/colors/test.json", color_definitions)
import_color_definitions("x11", "caas/colors/x11_rgb.json", color_definitions)
import_color_definitions("xkcd", "caas/colors/xkcd.json", color_definitions)
