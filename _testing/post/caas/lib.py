import datetime
import uuid
import numpy as np
import json
import caas
import pathlib


class WorkingFolder(object):

    def __init__(self):
        self.uuid = caas.lib.get_uuid()
        self.timestamp = caas.lib.get_timestamp()

        self.directory_name_of_current_image = self.timestamp + \
            "_" + str(self.uuid)

        self.filename_of_current_image = self.timestamp + \
            "_" + str(self.uuid) + ".jpg"

        self.path_and_filename_to_incoming_image = str(pathlib.PurePath(
            caas.storage_root,
            self.directory_name_of_current_image,
            self.filename_of_current_image))

        self.path_to_incoming_image = str(pathlib.PurePath(
            caas.storage_root,
            self.directory_name_of_current_image))

        pathlib.Path(self.path_to_incoming_image).mkdir(
            parents=True, exist_ok=True)

    def __repr__(self):

        s = ""

        s = s + "uuid: {}\n".format(
            self.uuid)
        s = s + "timestamp: {}\n".format(
            self.timestamp)
        s = s + "path_and_filename_to_incoming_image: {}\n".format(
            str(self.path_and_filename_to_incoming_image))
        s = s + "path_to_incoming_image: {}\n".format(
            str(self.path_to_incoming_image))

        return s


def color_to_json(scheme, index, rgb_from_image):

    rgb_from_scheme = caas.color_definitions[scheme]["rgbs"][index]

    diff = rgb_from_scheme - rgb_from_image

    returnDict = {
        'rgb': rgb_from_scheme.tolist(),
        'name': caas.color_definitions[scheme]["names"][index],
        'diff': diff.tolist(),
        'rgb_image': rgb_from_image
    }

    return returnDict


def get_uuid():
    return uuid.uuid4()


def get_timestamp():
    return datetime.datetime.now().isoformat().replace(':', '-')


def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist


def contains_markers(image):

    return False


def get_exif_from_jpg(pfnImage):

    return {}


def save_json(data, pfnOutFile):

    with open(pfnOutFile, 'w') as file:
        file.write(data)


def save_dict_as_json(data, pfnOutFile):

    with open(pfnOutFile, 'w') as file:
        json.dump(data, file)


def colormap_jet(n):
    r, g, b, = np.zeros(n), np.zeros(n), np.zeros(n)
    for i in range(0, n):
        m = 4.0*i/n
        r[i] = 255*min(max(min(m-1.5, -m+4.5), 0), 1)
        g[i] = 255*min(max(min(m-0.5, -m+3.5), 0), 1)
        b[i] = 255*min(max(min(m+0.5, -m+2.5), 0), 1)

    return np.uint8(np.c_[r, g, b])
