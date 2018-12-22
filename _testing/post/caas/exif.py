from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


def getCameraPropertiesAsDict(pfnImage):

    tags_dec = [40961, 37385, 37384, 40960, 41729, 41990, 41987, 50717,
                318, 36864, 34855, 41495, 271, 272, 305, 274, 40962, 40963, 531]

    img = Image.open(pfnImage)

    exif_dict = {}
    exif = img._getexif() or {}

    for tag_dec in tags_dec:
        tag_str = TAGS.get(tag_dec, tag_dec)
        value = exif.get(tag_dec, "undefined")
        # print("value: {:5d} , 0x{:05x}   tag: {} value: {}".format(tag_dec, tag_dec , tag_str, value))

        exif_dict[tag_str] = value

    return exif_dict


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def _process_ratios(value):
    """Helper function to convert the GPS ratios in float format"""
    return float(value[0])/float(value[1])


def _gps_tuple_processing(value):

    numValues = len(value)

    if(numValues == 2):
        # assume two integers: nominator and denominator
        return _process_ratios(value)

    if(numValues == 3):
        # assume three tuples of tuples of two
        return _convert_to_degress(value)

    return None


def _gps_process_time_tuple(value):

    h = int(_process_ratios(value[0]))
    m = int(_process_ratios(value[1]))
    # seconds remain float because of microseconds
    s = _process_ratios(value[2])

    return "{}:{}:{}".format(h, m, s)


def getLocationAsDict(pfnImage):

    img = Image.open(pfnImage)

    exif = img._getexif() or {}

    gps_tag_dec = 34853

    gps_dict = exif.get(gps_tag_dec, None)

    gpsinfo = {}

    for key in gps_dict.keys():
        decode = GPSTAGS.get(key, key)
        gps_value = gps_dict.get(key, None)

        if decode == 'GPSTimeStamp':
            gps_value = _gps_process_time_tuple(gps_value)

        if isinstance(gps_value, tuple):
            gps_value = _gps_tuple_processing(gps_value)

        if isinstance(gps_value, bytes):
            gps_value = gps_value.decode('utf-8')

        #print("tag: {}  value: {}  type of value: {}".format(
        #    decode, gps_value, type(gps_value)))

        gpsinfo[decode] = gps_value

    return gpsinfo
