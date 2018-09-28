import os
import cv2
import pathlib
import json

from random import randint

import caas.rgb_from_image_v1
import caas.rgb_from_image_v2
import caas.color_from_rgb_v1
import caas.lib


def rgb_from_image_dev(workingPath, imagePathFilename):

    returnDict = {
        "thumbnail": "na",
        "processing": "na",
        "rgb": [randint(0, 255), randint(0, 255), randint(0, 255)]
    }

    return returnDict


def process_main(path_to_current_image, path_and_filename_to_current_image):

    # make working dir
    timestamp = caas.lib.get_timestamp()

    workingPath = os.path.join(path_to_current_image, timestamp)

    pathlib.Path(workingPath).mkdir(parents=True, exist_ok=True)

    # here: determine wether image is an inquiry for color or a reference image
    # reference images have marker in it

    #  = check_for_marker(workingPath, imagePathFilename)

    # process image
    # result_image = rgb_from_image_dev(workingPath, imagePathFilename)
    result_image = caas.rgb_from_image_v2.run(
        workingPath, path_and_filename_to_current_image)

    # process colors
    result_color = caas.color_from_rgb_v1.run(
        workingPath, path_and_filename_to_current_image, result_image)

    # generate return value in case of errors
    # TBD

    returnDict = {}

    returnDict["version"] = {
        "number": "1.0.0",
        "description": "first version of result consolidation"
    }

    returnDict["results"] = {
        "workingPath": workingPath,
        "color": result_color
    }

    print(json.dumps(returnDict))

    # pfnReturnDict = os.path.join(workingPath, "return_dict.json.txt")
    # with open(pfnReturnDict, 'w') as file:
    #    #print(json.dumps(returnDict))
    #    file.write("test")#json.dumps(returnDict))

    return returnDict
