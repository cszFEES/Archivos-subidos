import requests
from bs4 import BeautifulSoup

#URL = "https://listado.mercadolibre.com.do/electrodomesticos-lavado/lavadora_ITEM*CONDITION_2230284_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondición%26applied_filter_order%3D3%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D23%26is_custom%3Dfalse"
#URL = "https://listado.mercadolibre.com.do/televisores/tv_ITEM*CONDITION_2230284_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondición%26applied_filter_order%3D2%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D129%26is_custom%3Dfalse"
URL = "https://inmuebles.mercadolibre.com.do/casas/venta/santo-domingo/santo-domingo-oeste/casa_PriceRange_1500000-9000000_NoIndex_True#applied_filter_id%3Dcity%26applied_filter_name%3DCiudades%26applied_filter_order%3D2%26applied_value_id%3DTVJEQ01SRFNBTlRPOA%26applied_value_name%3DSanto+Domingo+Oeste%26applied_value_order%3D7%26applied_value_results%3D113%26is_custom%3Dfalse"
URL = "https://inmuebles.mercadolibre.com.do/casas/venta/santo-domingo/casa_PriceRange_1500000-9000000_NoIndex_True#unapplied_filter_id%3Dcity%26unapplied_filter_name%3DCiudades%26unapplied_value_id%3DTVJEQ01SRFNBTlRPOA%26unapplied_value_name%3DSanto+Domingo+Oeste%26unapplied_autoselect%3Dfalse"
URL = "https://inmuebles.mercadolibre.com.do/casas/venta/distrito-nacional/casa_PriceRange_1500000-9000000_NoIndex_True#applied_filter_id%3Dstate%26applied_filter_name%3DUbicaci%C3%B3n%26applied_filter_order%3D3%26applied_value_id%3DTVJEUE1SRERJU1RSSQ%26applied_value_name%3DDistrito+Nacional%26applied_value_order%3D2%26applied_value_results%3D115%26is_custom%3Dfalse%26view_more_flag%3Dtrue"


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similaridadDelCoseno(texto1,texto2):
    vectorizer = CountVectorizer().fit_transform([texto1, texto2])
    cosine_sim = cosine_similarity(vectorizer[0], vectorizer[1])
    return float(cosine_sim)

def href(soupFind):
    link = str(soupFind)
    link = link[link.find("href"):]
    link = link[link.find("\"")+1:]
    link = link[:link.find("\"")]
    return link

def listadoDeLinks(URL):
    listaDeURLs = []
    while True:
        listaDeURLs.append(URL)
        try:
            r = requests.get(URL)
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            link = soup.find("li", class_="andes-pagination__button andes-pagination__button--next shops__pagination-button")
            link = str(link)
            link = link[link.find("href"):]
            link = link[link.find("\"")+1:]
            link = link[:link.find("\"")]
            URL = link
        except:
            return listaDeURLs        

def sacarInfo(URL):
    Lenunciados = []
    Lprecios = []
    Ltalla = []
    Lhabitaciones = []
    Lubicaciones = []
    Llinks = []
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    enunciados = soup.find_all("h2", class_="ui-search-item__title shops__item-title")
    precios = soup.find_all("span", class_="price-tag-text-sr-only")
    talla = soup.find_all("div", class_="ui-search-result__content-wrapper shops__result-content-wrapper")
    ubicaciones = soup.find_all("span", class_="ui-search-item__group__element ui-search-item__location shops__items-group-details")
    links = soup.find_all("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")
        
    for objeto in range(len(enunciados)):
        if precios[objeto].get_text()[precios[objeto].get_text().find(" "):] == " dólares"  :
            estePrecio = 55 * int(precios[objeto].get_text()[:precios[objeto].get_text().find(" ")])
        else:
            estePrecio = int(precios[objeto].get_text()[:precios[objeto].get_text().find(" ")])
        Lprecios.append(estePrecio)
        Lenunciados.append(enunciados[objeto].get_text())
        Lubicaciones.append(ubicaciones[objeto].get_text())
        Llinks.append(links[objeto].get('href'))
        

    for i in range(len(talla)):
        texto = talla[i].get_text()
        try:
            m2 = int(texto[texto.find("m²")-4:texto.find("m²")-1])
        except:
            m2 = 0
        try:
            habs = int(texto[texto.find("habs")-2:texto.find("habs")-1])
        except:
            habs = 0
        Ltalla.append(m2)
        Lhabitaciones.append(habs)

        
    return Lprecios,Lubicaciones,Ltalla,Lhabitaciones,Lenunciados, Llinks

def guardarInfoEnUnExcel(Lprecios,Lubicaciones,Ltalla,Lhabitaciones,Lenunciados, Llinks):
    import pandas as pd
    lista = [Lprecios,Lubicaciones,Ltalla,Lhabitaciones,Lenunciados, Llinks]
    ListaDeProductos = pd.DataFrame(lista, index=None)
    ListaDeProductos = ListaDeProductos.transpose()
    CantidadDeFilas = len(ListaDeProductos)
    print("Media =",ListaDeProductos[0].mean(),"          Cuantil =",ListaDeProductos[0].quantile([0.1]),   "Filas =",CantidadDeFilas)
                
    ListaDeProductos = ListaDeProductos.sort_values(by=ListaDeProductos.columns[0])
    ListaDeProductos = ListaDeProductos.replace('  ', ' ', regex=True)
    while True:
        repetidos1 = 0
        for i in reversed(range(CantidadDeFilas)):
            try:
                similitudUbi = similaridadDelCoseno(ListaDeProductos.iloc[i,1],ListaDeProductos.iloc[i-1,1])
                similitudDesc = similaridadDelCoseno(ListaDeProductos.iloc[i,4],ListaDeProductos.iloc[i-1,4])
                if (similitudUbi > 0.8) or (similitudDesc > 0.7):
                    ListaDeProductos.drop(i, axis=0, inplace=True)
                    repetidos1 = 1
            except:
                pass
        if repetidos1 == 0:
            break

    
    ListaDeProductos = ListaDeProductos.drop_duplicates()
    #ListaDeProductos[0] = ListaDeProductos[0].apply(lambda x: '{:,}'.format(x))
    ListaDeProductos.to_excel('output.xlsx', index=False)

    import openpyxl
    workbook = openpyxl.load_workbook('output.xlsx')
    worksheet = workbook.active
    worksheet['A1'] = 'Precio'
    worksheet.column_dimensions['A'].width = 14
    worksheet['B1'] = 'Ubicación'
    worksheet.column_dimensions['B'].width = 22
    worksheet['C1'] = 'm²'
    worksheet.column_dimensions['C'].width = 7
    worksheet['D1'] = 'Habs.'
    worksheet.column_dimensions['D'].width = 7
    worksheet['E1'] = 'Enunciado'
    worksheet.column_dimensions['E'].width = 7
    worksheet['F1'] = 'Links'
    workbook.save('output.xlsx')



def juntarInfo():
    Lenunciados = []
    Lprecios = []
    Ltalla = []
    Lhabitaciones = []
    Lubicaciones = []
    Llinks = []

    listaDeLinks = listadoDeLinks(URL) #obtener links
    for link in listaDeLinks:
        try:
            LpreciosTemporal,LubicacionesTemporal,LtallaTemporal,LhabitacionesTemporal,LenunciadosTemporal, LlinksTemporal = sacarInfo(link) #sacar info
        except:
            break
        Lenunciados.extend(LenunciadosTemporal)
        Lprecios.extend(LpreciosTemporal)
        Ltalla.extend(LtallaTemporal)
        Lhabitaciones.extend(LhabitacionesTemporal)
        Lubicaciones.extend(LubicacionesTemporal)
        Llinks.extend(LlinksTemporal)

    guardarInfoEnUnExcel(Lprecios,Lubicaciones,Ltalla,Lhabitaciones,Lenunciados,Llinks) #guardarExcel


def averiguarCoordenadas():    
    import pandas as pd
    tablaDeCasas = pd.read_excel("output.xlsx")
    listaDeCoordenadas = []

    from geopy.geocoders import ArcGIS
    import folium
    coordenadasDeSantoDomingo = [18.474747,-69.935208]
    mapaFinal = folium.Map(location= coordenadasDeSantoDomingo, zoom_start=10)

    import time as t
    cantidadDeLinks = len(tablaDeCasas.iloc[:, -1])
    for i in range(cantidadDeLinks):
        contadorDeFallosPorSiNoPusieronLasCoordenadas = 0
        while True:
            try:
                response = requests.get(tablaDeCasas.iloc[i,-1])
                html_content = response.content
                soup2 = BeautifulSoup(html_content, 'html.parser')

                estasCoordenadas = soup2.prettify()
                estasCoordenadas = estasCoordenadas[estasCoordenadas.find("center="):estasCoordenadas.find("&amp;zoom=")]
                c1 = estasCoordenadas[estasCoordenadas.find("="):estasCoordenadas.find("%2C")]
                c2 = estasCoordenadas[estasCoordenadas.find("C"):estasCoordenadas.find("&")]
                c1 = float(c1[1:])
                c2 = 0-float(c2[2:])
                estasCoordenadas = [c1,c2]
                listaDeCoordenadas.append(estasCoordenadas)
                break
            except:
                t.sleep(1)
                if contadorDeFallosPorSiNoPusieronLasCoordenadas > 9:
                    lugar = ArcGIS().geocode(tablaDeCasas.iloc[i,1])
                    estasCoordenadas = [float(lugar.latitude), float(lugar.longitude)]
                    listaDeCoordenadas.append(estasCoordenadas)
                    break
                contadorDeFallosPorSiNoPusieronLasCoordenadas += 1
                pass

        folium.Marker(
                location= estasCoordenadas,
                popup=str(format(int(tablaDeCasas.iloc[i,0]), ','))+"\n"+str(tablaDeCasas.iloc[i,-1])
            ).add_to(mapaFinal)
        print(i+1,"/",cantidadDeLinks)

    tablaDeCasas["Coordenadas"] = listaDeCoordenadas
    
    import numpy as np
    listaDeCoordenadas = np.array(listaDeCoordenadas)
                                   
    from sklearn.cluster import KMeans
    import math
    raizCuadradaCantidadDelinks = int(math.sqrt(cantidadDeLinks))
    kmeans = KMeans(n_clusters = raizCuadradaCantidadDelinks) 
    kmeans.fit(listaDeCoordenadas)
    labels = kmeans.labels_
    tablaDeCasas["Clúster de ubicaciones"] = labels

    precioPorMetroCuadrado = []
    for i in range(cantidadDeLinks):
        precioPorMetroCuadrado.append(int(tablaDeCasas.iloc[i,0]) / (int(tablaDeCasas.iloc[i,2])+1))
    tablaDeCasas["precioPorMetroCuadrado"] = precioPorMetroCuadrado

    kmeans = KMeans(n_clusters = raizCuadradaCantidadDelinks)  
    kmeans.fit(listaDeCoordenadas)
    labels = kmeans.labels_
    tablaDeCasas["Clúster de S/M"] = labels
    
    tablaDeCasas.to_excel("output.xlsx", index = False)
    mapaFinal.save('mapa de precios de casas.html')


print("Este archivo hace web scrap, guarda la info en un excel llamado output.xlsx y ubica esa info en un mapa llamado mapa_de_precios.html")
juntarInfo()
averiguarCoordenadas()

