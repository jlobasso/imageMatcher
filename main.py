import cv2

# https://http2.mlstatic.com/mochila-nike-elemental-negra-importada-original-ba5405010-D_NQ_NP_753682-MLA28367807721_102018-O.webp

 
#Cargamos las dos imagenes para hacer las diferencias

diff1 = cv2.imread('images/Z2bis.jpeg') # trainImage
diff2 = cv2.imread('images/Z2.jpeg') # queryImage
# diff1 = cv2.imread('images/mochila-nike-elemental-negra-importada-original-ba5405010-D_NQ_NP_753682-MLA28367807721_102018-O.webp')
# diff2 = cv2.imread('images/mochila-nike-elemental-negra-importada-original-ba5405010-D_NQ_NP_753682-MLA28367807721_102018-O.webp')
 
#Calculamos la diferencia absoluta de la dos imagenes
diff_total = cv2.absdiff(diff1, diff2)
diff = cv2.subtract(diff1, diff2)

imgray = cv2.cvtColor(diff1,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(diff2, contours, -1, (0,255,0), 1)

cv2.imwrite("/home/mich/workspace/imageMatcher/images/Fotodif.jpg", diff1)
 
#Buscamos los contornos
imagen_gris = cv2.cvtColor(diff_total, cv2.COLOR_BGR2GRAY)
contours,_ = cv2.findContours(imagen_gris,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 
#Miramos cada uno de los contornos y, si no es ruido, dibujamos su Bounding Box sobre la imagen original
for c in contours:
    if cv2.contourArea(c) >= 20:
        posicion_x,posicion_y,ancho,alto = cv2.boundingRect(c) #Guardamos las dimensiones de la Bounding Box
        cv2.rectangle(diff1,(posicion_x,posicion_y),(posicion_x+ancho,posicion_y+alto),(0,0,255),2) #Dibujamos la bounding box sobre diff1
 
while(1):
    cv2.imshow('Imagen1', diff1)
    cv2.imshow('Imagen2', diff2)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()

