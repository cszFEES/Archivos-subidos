import cv2, numpy

name = "metaur.png" #zeroprueba.png
imagen = cv2.imread(name)
codigo = numpy.array(imagen) #numpy guarda las yes en las equis  sprite-megaman-zero-sprite.png

"""
import matplotlib.pyplot as plt
plt.imshow(imagen)
plt.show()
with open("resultado.txt", "w") as f:
    f.write(str(sprite))
"""

PixelesX = []
PixelesY = []
ColoresHex = []

#print(str(len(codigo))+"x"+str(len(codigo[1]))+"pixeles", "--> ancho por alto\n")

def uno():
    for i in range(len(codigo)):
        lineaHorizontal = codigo[i]
        for j in range(len(lineaHorizontal)):
            pixelActual = lineaHorizontal[j]   #RGBmaestro es el pixel actual
            if pixelActual[0]<3 and pixelActual[1]<3 and pixelActual[2]<3:
                pass
            elif pixelActual[0]>250 and pixelActual[1]>250 and pixelActual[2]>250:
                pass
            elif pixelActual[0]==51 and pixelActual[1]==51 and pixelActual[2]==0:  #Para borrar los verdes de Zero
                pass
            else:
                R = str(hex(pixelActual[2]))
                G = str(hex(pixelActual[1]))
                B = str(hex(pixelActual[0]))
                RGB = "#"+ R[2:] + G[2:] + B[2:]
                PixelesX.append(j)
                PixelesY.append(i)
                ColoresHex.append(RGB)
                sprite = [PixelesX,PixelesY,ColoresHex]
    #print("\nvar PixelesX =",PixelesX,"\n\nvar PixelesY =",PixelesY,"\n\nvar ColoresHex =",ColoresHex)
    print("var sprite =\n",sprite)
    

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
