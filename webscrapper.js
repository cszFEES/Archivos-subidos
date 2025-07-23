const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises; // usar la versión promise de fs para async/await

const url = 'https://historyreviewed.best/';
const archivoLinks = 'links.txt'; // archivo donde guardar los links

async function principal() {
  let enlacesGuardados = new Set();

  // Leer links guardados si el archivo existe
  try {
    const data = await fs.readFile(archivoLinks, 'utf-8');
    const linksPrevios = data.split('\n').filter(Boolean);
    enlacesGuardados = new Set(linksPrevios);
    console.log(`Cargados ${enlacesGuardados.size} enlaces previamente guardados.`);
  } catch (err) {
    if(err.code === 'ENOENT') {
      console.log('Archivo de links no encontrado, se creará uno nuevo.');
    } else {
      console.error('Error leyendo archivo de links:', err.message);
      return;
    }
  }

  try {
    const respuesta = await axios.get(url);
    const html = respuesta.data;
    const $ = cheerio.load(html);

    const elementosArticulo = $('h3.entry-title a');

    for (const elemento of elementosArticulo.toArray()) {
      const titulo = $(elemento).text().trim();

      if (titulo.startsWith("Video:")) {
        const enlace = $(elemento).attr('href');
        try {
          const respuestaArticulo = await axios.get(enlace);
          const htmlArticulo = respuestaArticulo.data;
          const $$ = cheerio.load(htmlArticulo);

          const enlaceYoutubeElemento = $$('div.entry-content.clearfix p a[href*="youtube.com"]');

          if (enlaceYoutubeElemento.length > 0) {
            const urlYoutube = enlaceYoutubeElemento.attr('href');

            if (enlacesGuardados.has(urlYoutube)) {
              break; // lo que quedan son links viejos
            }

            console.log(`Nuevo YouTube: ${urlYoutube}\n`);

            // Añadir a enlaces guardados y guardar en archivo
            enlacesGuardados.add(urlYoutube);
            await fs.appendFile(archivoLinks, urlYoutube + '\n');

          } else {
            console.log(`No se encontró enlace de YouTube en el artículo.\n`);
          }
        } catch (error) {
          console.error(`Error accediendo al artículo ${enlace}: `, error.message);
        }
      }
    }
  } catch (error) {
    console.error('Error obteniendo la página principal:', error.message);
  }
}

principal();
