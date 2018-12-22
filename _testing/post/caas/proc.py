import os
import cv2
import pathlib
import json

from random import randint

import caas.rgb_from_image
import caas.color_from_rgb
import caas.lib


def rgb_from_image_dev(workingPath, imagePathFilename):

    returnDict = {
        "thumbnail": "na",
        "processing": "na",
        "rgb": [randint(0, 255), randint(0, 255), randint(0, 255)]
    }

    return returnDict


def process_main(
    path_working,
    path_and_filename_to_current_image):

    # at this stage: extract exif properties as jon and store in working dir
    
    
    # at this stage: determine wether image is an inquiry for color or a reference image
    # reference images have marker in it

    #  = check_for_marker(workingPath, imagePathFilename)

    # process image
    # result_image = rgb_from_image_dev(workingPath, imagePathFilename)
    result_image = caas.rgb_from_image.run(
        path_working, path_and_filename_to_current_image)

    # process colors
    result_color = caas.color_from_rgb.run(
        path_working, path_and_filename_to_current_image, result_image)

    # generate return value in case of errors
    # TBD

    returnDict = {}

    returnDict["version"] = {
        "number": "1.0.0",
        "description": "first version of result consolidation"
    }

    returnDict["results"] = {
        "workingPath": path_working,
        "color": result_color
    }

    print("processing result:")
    print(json.dumps(returnDict))

    pfnOutFile = os.path.join(path_working, "processing.json")
    
    caas.lib.save_dict_as_json(returnDict, pfnOutFile)
    
    return returnDict
