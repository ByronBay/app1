import os
import caas

folders = []
files = []


for entry in os.scandir('.'):

    if not entry.is_dir():
        continue

    first_n_cahr = entry.path[0:5]

    # any path with 201 in the beginning is most likely a path with an image to process in
    if first_n_cahr.find("201") < 0:
        continue

    imagePath = entry.path
    imagePathFilename = os.path.join(imagePath, imagePath[2:]+'.jpg')

    print(imagePathFilename)

    #rgb = [171, 195, 218]
    #result_to_phone = caas.proc.process_colors(rgb)

    result_to_phone = caas.proc.process_main(imagePath, imagePathFilename)

    print(result_to_phone)
