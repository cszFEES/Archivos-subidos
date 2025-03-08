from playwright.sync_api import sync_playwright
from time import sleep as t
import json

class ManejarJson:
    def __init__(self, vetados_file="autoresVetados.json"):
        self.vetados_file = vetados_file
        self._ensure_vetados_file()
    def cargar_json(self, nombre: str):
        try:
            with open(f"{nombre}.json", "r") as file:
                listado = json.load(file)
        except FileNotFoundError:
            listado = []
        return listado
    def guardar_json(self, listado: list, nombre: str):
        with open(f"{nombre}.json", "w") as file:
            json.dump(listado, file, indent=4)
    def vetar_autores(self, nombre: str):
        listado = self.cargar_json(self.vetados_file.replace(".json", "")) #remove .json to load the vetados file.
        listado.append(nombre)
        listado = list(set(listado))
        self.guardar_json(listado, self.vetados_file.replace(".json", "")) #remove .json to save the vetados file.    



def clips_scrapper(url:str, numPaginas:int):
  import langdetect, emoji
  """from translate import Translator
  translator = Translator(to_lang='en')"""

  def cancelar_titulo(titulo: str):
    try:
      titulo = titulo.lower()
      idioma_sudaca:bool = langdetect.detect(titulo) == "pt" or langdetect.detect(titulo) == "es"
      banned_words:list = ['xd',':d','merry','happy','gg','@','))',' o ',' do ',' de ','cs2','...','??','!!','sex','ass','fuck','discord','lmao','jaja','kkkk']
      inepto:bool =  any(titulo.find(word) != -1 for word in banned_words)
      emojis:bool = emoji.emoji_count(titulo) > 0
      return idioma_sudaca or inepto or emojis
    except:
      return True
    

  with sync_playwright() as p:
      browser = p.firefox.launch(headless= False)
      page = browser.new_page()

      page.route("**/*", lambda route: route.abort() 
        if route.request.resource_type == "image"
        else route.continue_()
      )
      page.goto(url)
      while page.title().find("Today") < 0:
        t(2)
      page.wait_for_load_state("load")
      t(1)
      titulos, autores, links = [], [], []
      autoresVetados = ManejarJson.cargarJson('autoresVetados')
      linksUsados = ManejarJson.cargarJson('linksUsados')

      for i in range(numPaginas): #5 usualmente
          miniaturas = page.locator('li.clli').all()
          for miniatura in miniaturas:
            titulo = miniatura.locator('div.contitle').inner_text()
            if cancelar_titulo(titulo):
              continue
            '''if any(not 'LATIN' in unicodedata.name(letra, '') for letra in titulo if letra.isalpha()):
              titulo =  'english: ' + translator.translate(titulo)'''
            autor = miniatura.locator('div.constreamer').inner_text()
            if autor in autoresVetados:
              continue
            link = miniatura.locator('div.conslug a').first.get_attribute('href')
            link = 'https://clips.twitch.tv/' + link.split("/")[-1]
            if link in linksUsados:
              continue
            #print(titulo, autor, link)
            titulos.append(titulo)
            autores.append(autor)
            links.append(link)
          try:
            page.locator('a.ldchrt:has-text("NEXT")').click(timeout=3000); t(0.2)
            page.wait_for_load_state("load")
          except Exception as e:
            print(e)
            break
      browser.close()
      linksUsados = links
      ManejarJson.guardarJson(listado=linksUsados,nombre="linksUsados")

      return titulos, autores, links

if False: # Para probar este código
  url = "https://twitchstats.net/clips/game/Super Smash Bros. Ultimate"
  videos = clips_scrapper(url, 2)