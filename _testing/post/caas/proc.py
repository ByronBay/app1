import os
import cv2
import pathlib
import caas
from scipy import spatial
import numpy as np
import json

def color_to_json(scheme, index, rgb):

    returnDict = {
        'rgb': caas.color_definitions[scheme]["rgbs"][index],
        'name': caas.color_definitions[scheme]["names"][index],
        'diff': caas.color_definitions[scheme]["rgbs"][index]-rgb
    }

    return returnDict


def color_from_rgb(workingPath, imagePathFilename, result_image):

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
        p1 = color_to_json(color_scheme, index[0], rgb_values)
        p2 = color_to_json(color_scheme, index[1], rgb_values)
        p3 = color_to_json(color_scheme, index[2], rgb_values)

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
        "best": {
            "name": color_scheme_result[color_scheme_bestfit]["p1"]["name"],
            "rgb": color_scheme_result[color_scheme_bestfit]["p1"]["rgb"],
            "diff": color_scheme_result[color_scheme_bestfit]["p1"]["diff"],
            "scheme": color_scheme_bestfit
        }
    }

    return color


# imagePath, imagePathFilename

def rgb_from_image(workingPath, imagePathFilename):

    # load image
    print("Load image : " + imagePathFilename)

    img = cv2.imread(imagePathFilename, cv2.IMREAD_COLOR)

    # make thumbnail, possibly for downloading to phone
    thumbnail = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

    pfnThumbnail = os.path.join(workingPath, "thumbnail.png") 

    cv2.imwrite( pfnThumbnail, thumbnail)

    # cur out inner third 
    imgProc = cv2.resize(img, (128*3, 128*3), interpolation=cv2.INTER_CUBIC)
    imgProc = imgProc[128:256, 128:256]

    pfnProc = os.path.join(workingPath, "proc.png")

    cv2.imwrite(pfnProc, imgProc)

    
    # done
    return {
        "thumbnail": pfnThumbnail,
        "processing": pfnProc,
        "rgb" :[100, 150, 200] 
    }
    


def process_main(imagePath, imagePathFilename):

    # make working dir
    timestamp = caas.lib.get_timestamp()

    workingPath = os.path.join(imagePath, timestamp)

    pathlib.Path(workingPath).mkdir(parents=True, exist_ok=True)

    # process image
    result_image = rgb_from_image(workingPath, imagePathFilename)

    # process colors
    result_color = color_from_rgb(workingPath, imagePathFilename, result_image)

    # generate return value in case of errors
    # TBD

    returnDict = {}

    returnDict["version"] = {
        "number": "1.0.0",
        "description": "first version of result consolidation"
    }

    returnDict["results"] = {
        "color": result_color
    }

    pfnReturnDict = os.path.join(workingPath, "return_dict.json.txt")

    #with open(pfnReturnDict, 'w') as file:
    #    #print(json.dumps(returnDict))
    #    file.write("test")#json.dumps(returnDict)) 

    return returnDict
