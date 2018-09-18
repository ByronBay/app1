import os
import cv2
import pathlib
import caas
from scipy import spatial


def color_to_json(scheme, index, rgb):

    returnDict = {
        'rgb': caas.color_definitions[scheme]["rgbs"][index],
        'name': caas.color_definitions[scheme]["names"][index],
        'diff': caas.color_definitions[scheme]["rgbs"][index]-rgb
    }

    return returnDict


def process_colors(rgb_values):

    cd = caas.color_definitions

    color = {}

    for color_scheme in cd.keys():
        print("processing {}".format(color_scheme))

        # compare against known colors
        RGB = cd[color_scheme]["rgbs"]

        # using function from scipy spatial library.
        dist, index = spatial.KDTree(RGB).query(rgb_values, 3)

        # make json structures
        p1 = color_to_json(color_scheme, index[0], rgb_values)
        p2 = color_to_json(color_scheme, index[1], rgb_values)
        p3 = color_to_json(color_scheme, index[2], rgb_values)

        color[color_scheme] =  {"p1": p1, "p2": p2, "p3": p3}
    
    return color


# imagePath, imagePathFilename

def process_image(workingPath, imagePathFilename):

    # load image
    print("Load image : " + imagePathFilename)

    img = cv2.imread(imagePathFilename, cv2.IMREAD_COLOR)

    thumbnail = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(os.path.join(workingPath, "thumbnail.jpg"), thumbnail)

    imgProc = cv2.resize(img, (128*3, 128*3), interpolation=cv2.INTER_CUBIC)

    cv2.imwrite(os.path.join(workingPath, "proc.jpg"), imgProc)

    return [100, 150, 200]


def process_main(imagePath, imagePathFilename):

    # make working dir
    timestamp = caas.lib.get_timestamp()

    workingPath = os.path.join(imagePath, timestamp)

    pathlib.Path(workingPath).mkdir(parents=True, exist_ok=True)

    # process image
    rgb = process_image(workingPath, imagePathFilename)

    # process colors
    returnDict = process_colors(rgb)

    # generate return value in case of errors
    # TBD

    return returnDict
