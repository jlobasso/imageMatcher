
from glob import glob


def getImages(path):
    # img = glob("../frontend/repo/joico/"+path+"/*")
    img = glob("/home/images-matcher/imageMatcher/frontend/repo/joico/"+path+"/*")
    return img
