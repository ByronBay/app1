from scipy import spatial
import numpy as np
import json

import caas


def run(workingPath, imagePathFilename, result_image):

    rgb_values = result_image["rgb"]

    cd = caas.color_definitions

    color_scheme_result = {}

    distances = np.empty([0])

    color_schemes = list(cd.keys())

    for color_scheme in color_schemes:
        print("processing {}".format(color_scheme))

        # compare against known colors
        RGB = cd[color_scheme]["rgbs"]

        # using function from scipy spatial library.
        dist, index = spatial.KDTree(RGB).query(rgb_values, 3)

        distances = np.append(distances, dist[0])

        # make json structures
        p1 = caas.lib.color_to_json(color_scheme, index[0], rgb_values)
        p2 = caas.lib.color_to_json(color_scheme, index[1], rgb_values)
        p3 = caas.lib.color_to_json(color_scheme, index[2], rgb_values)

        color_scheme_result[color_scheme] = {"p1": p1, "p2": p2, "p3": p3}

    color = {}

    color["version"] = {
        "number": "1.0.0",
        "description": "spatial.kdtree, three best candidates"
    }

    index_color_scheme_bestfit = np.argmin(distances)
    color_scheme_bestfit = color_schemes[index_color_scheme_bestfit]

    color["results"] = {
        "schemata": color_scheme_result,
        "rgbFromImage" : rgb_values,
        "best": {
            "name": color_scheme_result[color_scheme_bestfit]["p1"]["name"],
            "rgb": color_scheme_result[color_scheme_bestfit]["p1"]["rgb"],
            "diff": color_scheme_result[color_scheme_bestfit]["p1"]["diff"],
            "scheme": color_scheme_bestfit
        }
    }

    print("color_from_rgb_result:")
    print(json.dumps(color))

    return color
