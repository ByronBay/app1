import os
import cv2
import pathlib
import caas
from scipy import spatial


def process_colors(rgb_values):

    cd = caas.color_definitions

    # compare against known colors
    RGB = cd["x11"]["rgbs"]
    # using function from scipy spatial library.
    NearestRGB = (RGB[spatial.KDTree(RGB).query(rgb_values)[1]])

    returnDict = {
        'version': "1.0.0",
        'rgb': {'value': rgb_values, 'confidence': 500},
        'ral': {'value': 12002, 'confidence': 0},
        'fashion': {'value': 'peach', 'confidence': 200}
    }

    return returnDict


#imagePath, imagePathFilename

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
