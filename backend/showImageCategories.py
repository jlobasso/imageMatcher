from function.start import *
from categoriesForImage import *

config = configparser.ConfigParser()
config.read('conf.ini')

conn = MongoClient()
db = conn.imageMatcher

def showImageCategories(params):

    collections = [params.get('storageX')]
    categories = [params.get('categoriesStorageX')]
    
    obteneCategorias = categoriesForImage(collections, categories)
    return obteneCategorias
   