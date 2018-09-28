import os
import caas.proc

folders = []
files = []


for entry in os.scandir('./data/'):

    if not entry.is_dir():
        continue

    imagePath = entry.path
    imagePathFilename = os.path.join(imagePath, imagePath[7:]+'.jpg')

    print("imagePathFilename  : {}".format(imagePathFilename))

    #rgb = [171, 195, 218]
    #result_to_phone = caas.proc.process_colors(rgb)

    result_to_phone = caas.proc.process_main(imagePath, imagePathFilename)

    print(result_to_phone)
