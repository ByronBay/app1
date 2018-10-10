import os
import caas.proc

folders = []
files = []


for entry in os.scandir('./data_dev/'):

    if not entry.is_dir():
        continue

    imagePath = entry.path
    imagePathFilename = os.path.join(imagePath, imagePath[11:]+'.jpg')

    print("imagePath          : {}".format(imagePath))
    print("imagePathFilename  : {}".format(imagePathFilename))

    result_to_phone = caas.proc.process_main(imagePath, imagePathFilename)

    print(result_to_phone)
