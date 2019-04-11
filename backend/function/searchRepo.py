
from glob import glob


def getImages(path):
    img = glob("repo/joico/"+path+"/*")
    return img
