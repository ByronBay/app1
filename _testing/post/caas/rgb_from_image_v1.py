import cv2
import os
import numpy as np
import json
import caas.lib
from sklearn.cluster import KMeans
from sklearn import metrics


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

    imgProc = cv2.medianBlur(imgProc, 5)

    pfnProc = os.path.join(path_to_current_image, "proc.png")

    cv2.imwrite(pfnProc, imgProc)

    ####

    clusters = 3

    # Reshape the image to be a list of pixels
    image_array = imgProc.reshape((imgProc.shape[0] * imgProc.shape[1], 3))
    print(image_array)
    # Clusters the pixels
    clt = KMeans(n_clusters=clusters)
    clt.fit(image_array)

    print("clustering done")

    # Finds how many pixels are in each cluster
    hist = caas.lib.centroid_histogram(clt)

    print("histogram done")

    # Sort the clusters according to how many pixel they have
    # zipped = zip(hist, clt.cluster_centers_)
    # zipped.sort(reverse=True, key=lambda x: x[0])
    zipped = sorted(zip(hist, clt.cluster_centers_),
                    reverse=True, key=lambda x: x[0])

    hist, clt.cluster_centers = zip(*zipped)

    silhouette = metrics.silhouette_score(
        image_array, clt.labels_, metric='euclidean')

    print("Cluster: {} , Silhouette {}".format(clusters, silhouette))

    bgr = clt.cluster_centers[0]

    print("sorting done")

    # document color segments

    # CV_8UC1

    ### im_color = cv2.applyColorMap(
    ###    np.uint8(np.reshape(1+clt.labels_, (128, 128))),
    ###    caas.lib.colormap_jet(clusters))

    ### pfnSeg = os.path.join(path_to_current_image, "segments.png")

    ### cv2.imwrite(pfnSeg, im_color)

    ####

    returnDict = {
        "thumbnail": pfnThumbnail,
        "processing": pfnProc,
        "rgb": [bgr[2], bgr[1], bgr[0]]
    }

    print("rgb_from_image_v1 result:")
    print(json.dumps(returnDict))

    # done
    return returnDict
