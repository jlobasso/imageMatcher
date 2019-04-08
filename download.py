import numpy as np
import cv2
import urllib.request
import time
import json

def downloadImage(images):
    print(len(images))

    for x in range(0, len(images)):

        archivoDescargar = urllib.request.urlopen(images[x]['image'])
        # now = time.time()         
        
        img = str(images[x]['image'])[8:]
        img = img.replace("/", "_")

        print(str(x)+'_'+img)

        ficheroGuardar = open('joico/imgAnuncio/'+str(x)+'_'+img,"wb")
        ficheroGuardar.write(archivoDescargar.read())
        ficheroGuardar.close()    

        # elapsed = time.time() - now        
# print ('Descargado el archivo: ' + archivoDescargar,elapsed)