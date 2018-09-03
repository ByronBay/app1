import os
import cv2
import pathlib
import caas.aux

def process_color_engine(image):

    returnDict = {
                'version' : "1.0.0",
                'rgb' : { 'value': [1,2,4], 'confidence' : 500},
                'hsv' : {'value' : [3,4,5], 'confidence' : 400},
                'ral' : {'value' : 12002, 'confidence' : 0},
                'fashion' : {'value' : 'peach', 'confidence' : 200}
            }

    return returnDict



def process_image(dataDir, pfnImage):

    #make working dir
    timestamp = caas.aux.get_timestamp()

    workingDir = os.path.join(dataDir, timestamp)

    pathlib.Path(workingDir).mkdir(parents=True, exist_ok=True)

    # load image
    print("Load image : " + pfnImage)

    img = cv2.imread(pfnImage, cv2.IMREAD_COLOR)

    thumbnail = cv2.resize(img,(128, 128), interpolation = cv2.INTER_CUBIC)

    cv2.imwrite( os.path.join(workingDir, "thumbnail.jpg"), thumbnail)

    imgProc = cv2.resize(img,(128*3, 128*3), interpolation = cv2.INTER_CUBIC)

    cv2.imwrite( os.path.join(workingDir, "proc.jpg"), imgProc)

    # process image
    returnDict = process_color_engine(imgProc)
    # generate return value
    
    return returnDict
