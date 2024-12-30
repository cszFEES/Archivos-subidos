import json

def cargarJson(nombre:str):
    try:
        with open(f"{nombre}.json", "r") as file:
            listado = json.load(file)
    except:
        listado = []
    return listado

def guardarJson(listado:list, nombre:str):
    with open(f"{nombre}.json", "w") as file:
        json.dump(listado, file, indent=4)
