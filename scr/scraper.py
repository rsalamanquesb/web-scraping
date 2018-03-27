from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import numpy as np
import pandas as pd

from ipwhois import IPWhois

class ReservasHidraulicas:

    def __init__(self):
        self.url1 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date='
        self.url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date='
        self.url3 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date='

        #self.urlBase = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60000&screen_language=&bh_number=10&bh_year=2018&bh_date=02/03/2018'

        #A la urlBase habrá que añadirle las fechas uqe introduzca el usuario
        self.urlBase = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60000&screen_language=&bh_number=10&bh_year=2018&bh_date='
        self.fechaIni = '2018-02-27'
        self.fechaFin = '2018-03-05'
        self.fechas = []
        self.coleccionURLdePartida = []
        self.coleccionURLconDatos = []

    def cargarArrayFechas(self):

        fechasAux = np.arange(self.fechaIni, self.fechaFin, dtype='datetime64[D]')

        for fecha in fechasAux:
            #print(fecha)
            ts = pd.to_datetime(str(fecha))
            #print(ts)
            fechaFormateada = ts.strftime('%d/%m/%Y')
            self.fechas.append(fechaFormateada)
            #print(fechaFormateada)

    def get_html(self, url):
        html = urlopen(url).read()
        return html

    def cargarColeccionURLdePartida(self):

        self.cargarArrayFechas()

        for fecha in self.fechas:
            auxUrlBase = self.urlBase+fecha
            print("Agregada URL para búsqueda: " + auxUrlBase)
            self.coleccionURLdePartida.append(auxUrlBase)

    def tratarTexto(self, texto):

        texto = texto.replace(u'\xa0', '')
        texto = texto.replace('\n', ' ')
        texto = texto.replace('\t', ' ')
        texto = texto.strip()

        return texto

    def printInfoURL(self, url):

        result = IPWhois(url)
        print(result.address)

    def tratarURL(self, url):

        html = urlopen(url).read()

        cabecera1 = []
        cabecera2 = []
        datos = []

        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table',
                          {"width": "90%", "cellspacing": "1", "cellpadding": "1", "border": 0, "align": "center"})

        tr = table.find_all('tr')

        for i in range(0, len(tr)):

            # Inicialización para el bucle tr
            td = tr[i].find_all('td')
            linea = []

            for n in range(0, len(td)):
                if i == 0:
                    # Rellenar la cabecera1
                    cabecera1.append(self.tratarTexto(td[n].text))
                elif i == 1:
                    # Rellenar la cabecera2
                    cabecera2.append(self.tratarTexto(td[n].text))
                else:
                    # Rellenar datos de la fila
                    linea.append(self.tratarTexto(td[n].text))

            if i > 1:
                # Añadir fila a la matriz de filas
                datos = datos + [linea]

        # Obtener la zona hidrográfica
        zona = self.tratarTexto(soup.find('td', {"class": "tdsubtitulo"}).text)

        #Imprimimos la información obtenida de la url tratada
        print(zona)
        print(cabecera1)
        print(cabecera2)
        print(datos,'\n')

    def scrape(self,url):

        #self.printInfoURL('http://eportal.mapama.gob.es/BoleHWeb/')
        self.tratarURL(url)

    def cargaColeccionURL(self):
        #Aquí vendrá el código que nos permita recorrer las webs que queremos procesar

        #Cargamos las tres url de ejemplo que tenemos
        self.coleccionURL.append(self.url1)
        self.coleccionURL.append(self.url2)
        self.coleccionURL.append(self.url3)

    def tratarColeccionURL(self):

        for n in range(0, len(self.coleccionURL)):
            self.scrape(self.coleccionURL[n])