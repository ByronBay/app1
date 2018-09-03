import os
import caas
 
folders = []
files = []
 
for entry in os.scandir('.'):
    
    if not entry.is_dir() :
        continue

    if entry.path[0:5] != "./201":
        continue 

    directoryServer = entry.path
    pfnImageServer = os.path.join(directoryServer, directoryServer[2:]+'.jpg')

    print (pfnImageServer)

    caas.proc.process_image(directoryServer, pfnImageServer)