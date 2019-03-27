import cv2
import numpy as np
 
imagen = cv2.imread('../images/n0p8.jpeg')
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)


#Rango de colores detectados:
#Verdes:
verde_bajos = np.array([49,50,50])
verde_altos = np.array([107, 255, 255])

#Azules:
azul_bajos = np.array([100,65,75], dtype=np.uint8)
azul_altos = np.array([130, 255, 255], dtype=np.uint8)


#Rojos:
rojo_bajos1 = np.array([0,65,75], dtype=np.uint8)
rojo_altos1 = np.array([12, 255, 255], dtype=np.uint8)
rojo_bajos2 = np.array([240,65,75], dtype=np.uint8)
rojo_altos2 = np.array([256, 255, 255], dtype=np.uint8)

#Crear las mascaras
mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)

#Juntar todas las mascaras
mask = cv2.add(mascara_rojo1, mascara_rojo2)
mask = cv2.add(mask, mascara_verde)
mask = cv2.add(mask, mascara_azul)

#Mostrar la mascara final y la imagen
cv2.imshow('Finale', mask)
cv2.imshow('Imagen', imagen)
 
#Salir con ESC
while(1):
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()


# # Algoritmo de deteccion de colores multiples
# # Busca los píxeles rojos, verdes y azules de una imagen
 
# import cv2
# import numpy as np
 
# imagen = cv2.imread('opencv_logo.png')
# hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
 
# #Rango de colores detectados:
# #Verdes:
# verde_bajos = np.array([49,50,50])
# verde_altos = np.array([107, 255, 255])
# #Azules:
# azul_bajos = np.array([100,65,75], dtype=np.uint8)
# azul_altos = np.array([130, 255, 255], dtype=np.uint8)
# #Rojos:
# rojo_bajos1 = np.array([0,65,75], dtype=np.uint8)
# rojo_altos1 = np.array([12, 255, 255], dtype=np.uint8)
# rojo_bajos2 = np.array([240,65,75], dtype=np.uint8)
# rojo_altos2 = np.array([256, 255, 255], dtype=np.uint8)
 
 
 
# #Crear las mascaras
# mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
# mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
# mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
# mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)
 
# #Juntar todas las mascaras
# mask = cv2.add(mascara_rojo1, mascara_rojo2)
# mask = cv2.add(mask, mascara_verde)
# mask = cv2.add(mask, mascara_azul)
 
# #Mostrar la mascara final y la imagen
# cv2.imshow('Finale', mask)
# cv2.imshow('Imagen', imagen)
 
# #Salir con ESC
# while(1):
#     tecla = cv2.waitKey(5) & 0xFF
#     if tecla == 27:
#         break
 
# cv2.destroyAllWindows()