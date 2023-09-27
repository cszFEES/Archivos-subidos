import requests
from bs4 import BeautifulSoup
import pandas as pd

enlace = "https://archlinux.org/packages/?page=1&sort=&q=python&maintainer=&flagged="
def navegadorDeLaPaginaDeAUR(paginaDeAUR):
    response = requests.get(paginaDeAUR)
    soup = BeautifulSoup(response.content, "html.parser")

    cuadroPrincipal= soup.find("tbody")
    links = cuadroPrincipal.find_all("a")
    descs = cuadroPrincipal.find_all(class_="wrap")
    dfTemporal = pd.DataFrame({"Module": [link.get_text() for link in links],"Description": [desc.get_text() for desc in descs], "Links": ["https://archlinux.org/packages"+link.get("href") for link in links]})
    try:
        enlace = "https://archlinux.org/packages/"+soup.find("a", title="Go to next page").get("href")
    except:
        enlace = 0
    return dfTemporal, enlace

df = pd.DataFrame(columns = ("Module","Description", "Links"))
while enlace != 0:
    dfTemporal, enlace = navegadorDeLaPaginaDeAUR(enlace)
    df = pd.concat([df,dfTemporal])
df = df[df['Module'].str.contains('python-')]
df.to_excel("aur.xlsx", index=False)