import cv2
 
#Cargamos las dos imagenes para hacer las diferencias
diff1 = cv2.imread('../repo/pruebaZ2.jpeg')
diff2 = cv2.imread('Z4.jpeg')
 
#Calculamos la diferencia absoluta de las dos imagenes
diff_total = cv2.absdiff(diff1, diff2)
 
#Buscamos los contornos
imagen_gris = cv2.cvtColor(diff_total, cv2.COLOR_BGR2GRAY)
contours,_ = cv2.findContours(imagen_gris,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 
#Miramos cada uno de los contornos y, si no es ruido, dibujamos su Bounding Box sobre la imagen original
for c in contours:
    if cv2.contourArea(c) >= 20:
        posicion_x,posicion_y,ancho,alto = cv2.boundingRect(c) #Guardamos las dimensiones de la Bounding Box
        cv2.rectangle(diff1,(posicion_x,posicion_y),(posicion_x+ancho,posicion_y+alto),(0,0,255),2) #Dibujamos la bounding box sobre diff1
 
while(1):
    #Mostramos las imagenes. ESC para salir.
    cv2.imshow('Imagen1', diff1)
    cv2.imshow('Imagen2', diff2)
    cv2.imshow('Diferencias detectadas', diff_total)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()