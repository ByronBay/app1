import datetime
import uuid
import numpy as np
import json
from caas import color_definitions


def color_to_json(scheme, index, rgb):

    rgb_array = caas.color_definitions[scheme]["rgbs"][index]

    rgb = rgb_array.tolist()

    diff_array = caas.color_definitions[scheme]["rgbs"][index]-rgb

    diff = diff_array.tolist()

    returnDict = {
        'rgb': rgb,
        'name': caas.color_definitions[scheme]["names"][index],
        'diff': diff
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
