import cv2
import numpy as np

name = "metaur.png" 
imagen = cv2.imread(name)
codigo = np.array(imagen)

R = []
G = []
B = []

def uno():
    lista = ""  
    for i in range(len(codigo)):
        lineaHorizontal = codigo[i]
        for j in range(len(lineaHorizontal)):
            pixelActual = lineaHorizontal[j]   #RGBmaestro es el pixel actual
            if pixelActual[0] < 5 and pixelActual[1] < 5 and pixelActual[2]  < 5:
                pass
            else:
                R.append(pixelActual[2])
                G.append(pixelActual[1])
                B.append(pixelActual[0])
    RGB = [R,G,B]
    print(R,G,B)


def multi():
    spriteNum = 0
    for i in range(len(codigo)):  
        lineaHorizontalActual = codigo[i]  #posici x
        for j in range(len(codigo[1])):   #posici x&y
            pixelActual = lineaHorizontalActual[j]
            if pixelActual[0] == 0 and pixelActual[1] == 0 and pixelActual[2] == 0:
                try:
                    for k in range(len(lineaHorizontalActual)-j):  #cruzar hacia la derecha
                        pixelSiguiente = lineaHorizontalActual[j+k]
                        if pixelSiguiente[0] == 0 and pixelSiguiente[1] == 0 and pixelSiguiente[2] == 0:
                            for m in range(i+1,len(codigo[1])):  #bajar
                                try:
                                    lineaBajada = codigo[i+m]
                                    pixelActualBajado = lineaBajada[j]
                                    pixelSiguienteBajado = lineaBajada[j+k]
                                    contadorDeVacios = 0
                                    if pixelSiguienteBajado[0] == 0 and pixelSiguienteBajado[1] == 0 and pixelSiguienteBajado[2] == 0 and pixelActualBajado[0] == 0 and pixelActualBajado[1] == 0 and pixelActualBajado[2] == 0:
                                        for n in range(k):  #revisar lineas horizontales para que estén vacías pero con contenido dentro
                                            pixelProbado = lineaBajada[j+n]
                                            if pixelProbado[0] == 0 and pixelProbado[1] == 0 and pixelProbado[2] == 0:
                                                contadorDeVacios += 1
                                        if contadorDeVacios == k+1:
                                            spriteNum =+1
                                            opcionMulti(i,j,k,m,n,spriteNum) #llegado a este punto, las cuatro lineas bordes están vacías. Ahora hay que crear una matriz pequeña para indicar que aquí está el sprite.
                                                
                                    else:
                                        break
                                            
                                except:
                                    pass
                        else:
                            break
                except:
                    continue    
            else:
                continue

def opcionMulti(i,j,k,m,n,spriteNum):
    print("\n\nSprite número:",spriteNum)
    for a in range(m):  #arriba a abajo
        lineaHorizontalSprite = codigo[i+a]
        for b in range(k):   #izquierda a derecha
            pixelActualSprite = lineaHorizontalSprite[j+b]
            if pixelActualSprite[0] == 0 and pixelActualSprite[1] == 0 and pixelActualSprite[2] == 0:
                pass
            else:
                R = str(hex(pixelActual[2]))
                G = str(hex(pixelActual[1]))
                B = str(hex(pixelActual[0]))
                RGB = R[2:] + G[2:] + B[2:]
                print("ctx.fillRect(" ,b, ", " ,a, ", 1, 1); \n ctx.fillStyle = \"#"+str(RGB)+"\";")



uno()
