#prueba 1
try:
    NUMERO = float(input("LEER NUMERO\n"))
    while int(NUMERO) >= 2:
        NUMERO -= 2
        print(int(NUMERO))
except:
   print("Pruebe escribiendo un número")


#prueba 2
try:
    class PERSONA():
        def __init__(self, sexo, edad:int):
            self.SEXO = sexo
            self.EDAD = edad
    PERSONAS = []

    import random    #se puede reemplazar la lista PERSONAS por una propia
    print("LEER PERSONAS")
    for i in range(50):
        sexo = random.randint(0, 1) #int(input("0 para hembra, 1 para macho"))
        edad = random.randint(0, 80) #int(input("ingrese la edad"))
        PERSONAS.append(PERSONA(sexo=sexo,edad=edad))
    print("Porcentaje de personas mayores",len([p for p in PERSONAS if p.EDAD >= 18])/len(PERSONAS)*100,"%")
    print("Porcentaje de mujeres",len([p for p in PERSONAS if p.SEXO == 0])/len(PERSONAS)*100,"%")
except:
    print("Ha introducido un dato erróneo")
    pass

#prueba 3
try:
    HORASTRABAJADAS = float(input("LEER HORAS TRABAJADAS\n"))
    TARIFA = float(input("LEER TARIFA\n"))

    PAGO = HORASTRABAJADAS * TARIFA
    if HORASTRABAJADAS > 40:
        PAGO = PAGO + (HORASTRABAJADAS-40) * TARIFA * 0.5
    print(PAGO)
except:
   print("Pruebe insertando números")
