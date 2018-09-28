import cv2
import os

from sklearn.cluster import KMeans
from sklearn import metrics
from caas.lib import centroid_histogram
import numpy as np


def run(path_to_current_image, path_and_filename_to_current_image):

    # load image
    print("Load image : " + path_and_filename_to_current_image)

    img = cv2.imread(path_and_filename_to_current_image, cv2.IMREAD_COLOR)

    # make thumbnail, possibly for downloading to phone
    thumbnail = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)

    pfnThumbnail = os.path.join(path_to_current_image, "thumbnail.png")

    cv2.imwrite(pfnThumbnail, thumbnail)

    # cur out inner third
    imgProc = cv2.resize(img, (128*3, 128*3), interpolation=cv2.INTER_CUBIC)
    imgProc = imgProc[128:256, 128:256]

    pfnProc = os.path.join(path_to_current_image, "proc_rgb.png")
    cv2.imwrite(pfnProc, imgProc)

    ####

    # Reshape the image to be a list of pixels
    image_array = imgProc.reshape((imgProc.shape[0] * imgProc.shape[1], 3))
    print(image_array)

    silhouette_max = -1
    bgr_win = []

    for clusters in range(2, 11):

        # Clusters the pixels
        clt = KMeans(n_clusters=clusters)
        clt.fit(image_array)

        # Finds how many pixels are in each cluster
        hist = centroid_histogram(clt)

        # Sort the clusters according to how many pixel they have
        zipped = sorted(zip(hist, clt.cluster_centers_),
                        reverse=True, key=lambda x: x[0])

        hist, clt.cluster_centers = zip(*zipped)

        silhouette = metrics.silhouette_score(
            image_array, clt.labels_, metric='euclidean', sample_size=2500)

        bgr = clt.cluster_centers[0]

        if silhouette > silhouette_max:
            silhouette_max = silhouette
            bgr_win = bgr

        print("Cluster: {} , Silhouette: {}, bgr: {}".format(
            clusters, silhouette, bgr_win))

    print("iterating done, winning cluster-values:")
    print("Silhouette: {}, bgr: {}".format(silhouette_max, bgr_win))

    ####

    returnDict = {
        "thumbnail": pfnThumbnail,
        "processing": pfnProc,
        "rgb": [bgr_win[2], bgr_win[1], bgr_win[0]]
    }

    # done
    return returnDict
