import os
import zipfile
import tarfile
import rarfile

def extraer_zip(ruta_archivo, ruta_extraer, contraseña=None):
    with zipfile.ZipFile(ruta_archivo, 'r') as zip_ref:
        if contraseña:
            zip_ref.extractall(path=ruta_extraer, pwd=contraseña.encode('utf-8'))
        else:
            zip_ref.extractall(path=ruta_extraer)
def extraer_tar(ruta_archivo, ruta_extraer):
    with tarfile.open(ruta_archivo, 'r:*') as tar_ref:
        tar_ref.extractall(path=ruta_extraer)
def extraer_rar(ruta_archivo, ruta_extraer, contraseña=None):
    with rarfile.RarFile(ruta_archivo) as rar_ref:
        if contraseña:
            rar_ref.extractall(path=ruta_extraer, pwd=contraseña)
        else:
            rar_ref.extractall(path=ruta_extraer)

def extraer_archivos_en_directorio(directorio, contraseña=None):
    for raiz, dirs, archivos in os.walk(directorio):
        for archivo in archivos:
            ruta_archivo = os.path.join(raiz, archivo)
            if zipfile.is_zipfile(ruta_archivo):
                ruta_extraer = os.path.join(raiz, archivo.replace('.zip', ''))
                extraer_zip(ruta_archivo, ruta_extraer, contraseña)
            elif ruta_archivo.endswith(('.tar', '.gz', '.bz2', '.tar.gz', '.tar.bz2')):
                ruta_extraer = os.path.join(raiz, archivo.replace('.tar', '').replace('.gz', '').replace('.bz2', ''))
                extraer_tar(ruta_archivo, ruta_extraer)
            elif ruta_archivo.endswith('.rar'):
                ruta_extraer = os.path.join(raiz, archivo.replace('.rar', ''))
                extraer_rar(ruta_archivo, ruta_extraer, contraseña)

contraseña = ""
carpeta = ""
extraer_archivos_en_directorio(carpeta, contraseña)
