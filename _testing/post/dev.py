import os
import caas

folders = []
files = []


for entry in os.scandir('.'):

    if not entry.is_dir():
        continue

    first_n_cahr = entry.path[0:5]

    if first_n_cahr != "./201":
        continue

    directoryServer = entry.path
    pfnImageServer = os.path.join(directoryServer, directoryServer[2:]+'.jpg')

    print(pfnImageServer)

    caas.proc.process_main(directoryServer, pfnImageServer)
