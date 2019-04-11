import numpy as np
import cv2
import urllib.request
import time
import json

def downloadImage(images):

    print ('cantidad de imagenes a descargar: ',len(images))
    now = time.time()         
    for x in range(0, len(images)):

        archivoDescargar = urllib.request.urlopen(images[x]['image'])
        
        img = str(images[x]['image'])[8:]
        img = img.replace("/", "_")

        print(str(x)+'_'+img)

        ficheroGuardar = open('repo/joico/download/'+str(x)+'_'+img,"wb")
        ficheroGuardar.write(archivoDescargar.read())
        ficheroGuardar.close()    

    elapsed = time.time() - now        
    print ('tiempo de descarga total de archivos: ',elapsed)