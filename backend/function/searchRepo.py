
from glob import glob


def getImages(path):
    result = glob(config['paths']['storage-full-path']+path+"/*")
    # img = glob("../frontend/repo/joico/"+path+"/*")
    # img = glob("../../frontend/repo/joico/"+path+"/*")
    return result
