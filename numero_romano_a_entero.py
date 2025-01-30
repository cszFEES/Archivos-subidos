
def numero_romano_a_entero(numRomano: str) -> int:
    romanos = ['I','V','X','L','C','D','M']
    valores = [1,5,10,50,100,500,1000]
    valPresente = 0
    suma = 0
    print(numRomano[::-1])
    for char in numRomano[::-1]:
        valor = valores[romanos.index(char)]
        if valor >= valPresente:
            valPresente = valor
            suma += valor
        if valor < valPresente:
            suma -= valor
    print(suma)
    return suma
        
numero_romano_a_entero('MCDXCII')
