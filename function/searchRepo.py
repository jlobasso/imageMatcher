
from glob import glob


def getImages(path):
    img = glob("joico/"+path+"/*")
    return img
