import json
import re

# reference:
# https://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html


class ImageAcquisitionInformation:

    basicExif = {}
    gpsInformation = {}

    def __init__(self, pfnImage):
        self.pfnImage = pfnImage

    def getBasicExif(self):
        return json.dumps({})

    def getGpsInformation(self):
        return json.dumps({})

    def _extractGpsInformation(self):
        return True

    def _extractBasicExif(self):
        return True
