import datetime
import uuid
import numpy as np
import json
import caas
import pathlib


class FolderManager(object):

    image_subfolder = "in"
    attributes_filename = "attributes.json"

    def __init__(self):

        self.uuid = caas.lib.get_uuid()
        self.timestamp = caas.lib.get_timestamp()

    def create_folder_structure(self, directory_to_use=""):

        if not directory_to_use:
            # start new structure
            self.init_green_field()
            self.write_attributes()
        else:
            # veryfiy for being existing structure
            self.init_brown_field(directory_to_use)

    def init_brown_field(self, directory_to_use):
        
        # check for presence attribute file
        pfnAttribs = pathlib.Path(
            directory_to_use,
            self.attributes_filename) 
        isFile = pfnAttribs.is_file()

        if (isFile):
            # read attributes
            attribs = caas.lib.read_json_into_dict(str(pfnAttribs))
            
            # get image filename
            filename_image = attribs['filename_of_current_image']       
            
            # check for presence of image
            pfnImage = pathlib.Path(
                directory_to_use,
                self.image_subfolder,
                filename_image) 
            isFile = pfnImage.is_file()

            self.filename_of_current_image = filename_image

            self.root_path_to_incoming_image = directory_to_use

            self.path_to_incoming_image = str(pathlib.Path(
                self.root_path_to_incoming_image,
                self.image_subfolder))

            self.path_and_filename_to_incoming_image = str(pathlib.Path(
                self.path_to_incoming_image,
                self.filename_of_current_image))

            # path working
            self.path_working = str(pathlib.PurePath(
                self.root_path_to_incoming_image, self.timestamp))

            pathlib.Path(self.path_working).mkdir(
                parents=True, exist_ok=True)

    def write_attributes(self):
        
        dict = {
            'uuid': str(self.uuid),
            'timestamp_incoming': self.timestamp,
            'filename_of_current_image': self.filename_of_current_image
            }

        pfnAttributes = str(pathlib.PurePath(
            self.root_path_to_incoming_image,
            self.attributes_filename))

        caas.lib.save_dict_as_json(dict, pfnAttributes)

    def init_green_field(self):

        self.directory_name_of_current_image = self.timestamp + \
            "_" + str(self.uuid)

        self.filename_of_current_image = self.timestamp + \
            "_" + str(self.uuid) + ".jpg"

        # root path to incominng image and processing
        self.root_path_to_incoming_image = str(pathlib.PurePath(
            caas.storage_root,
            self.directory_name_of_current_image))

        # path to incoming image
        self.path_to_incoming_image = str(pathlib.PurePath(
            self.root_path_to_incoming_image,
            self.image_subfolder))

        pathlib.Path(self.path_to_incoming_image).mkdir(
            parents=True, exist_ok=True)

        # path working
        self.path_working = str(pathlib.PurePath(
            self.root_path_to_incoming_image, self.timestamp))

        pathlib.Path(self.path_working).mkdir(
            parents=True, exist_ok=True)

        # path and filename to incoming image
        self.path_and_filename_to_incoming_image = str(pathlib.PurePath(
            self.path_to_incoming_image,
            self.filename_of_current_image))

    def __repr__(self):

        s = ""

        s = s + "uuid: {}\n".format(
            self.uuid)
        
        s = s + "timestamp: {}\n".format(
            self.timestamp)
        
        s = s + "incoming root path: {}\n".format(
            str(self.root_path_to_incoming_image))

        s = s + "path_to_incoming_image: {}\n".format(
            str(self.path_to_incoming_image))
        
        s = s + "path_and_filename_to_incoming_image: {}\n".format(
            str(self.path_and_filename_to_incoming_image))
        
        s = s + "path_working: : {}\n".format(
            str(self.path_working))

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


def save_json(data, pfnOutFile):

    with open(pfnOutFile, 'w') as file:
        file.write(data)


def save_dict_as_json(dict, pfnOutFile):

    with open(pfnOutFile, 'w') as file:
        json.dump(dict, file)


def read_json_into_dict(pfnInFile):
    
    dict = {}
    
    with open(pfnInFile, 'r') as file:
        dict = json.load(file)

    return dict

def colormap_jet(n):
    r, g, b, = np.zeros(n), np.zeros(n), np.zeros(n)
    for i in range(0, n):
        m = 4.0*i/n
        r[i] = 255*min(max(min(m-1.5, -m+4.5), 0), 1)
        g[i] = 255*min(max(min(m-0.5, -m+3.5), 0), 1)
        b[i] = 255*min(max(min(m+0.5, -m+2.5), 0), 1)

    return np.uint8(np.c_[r, g, b])
