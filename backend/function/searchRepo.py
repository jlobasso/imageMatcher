import numpy as np
import cv2
from glob import glob
import configparser
import urllib.request

config = configparser.ConfigParser()
config.read('conf.ini')

def getImages(path):
    result = glob(config['paths']['storage-full-path']+path+"/*")
    return result

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image