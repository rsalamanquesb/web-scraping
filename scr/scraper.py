from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd

from ipwhois import IPWhois

class ReservasHidraulicas:

    def __init__(self):
        self.url1 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date='
        self.url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date='

        # self.url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
        #     'bh_number=10&bh_year=2018&bh_amb_name=%27+escape(%27Cuencas%20Internas%20de%20Catalu%C3%B1a%27)+%27&bh_amb_id=10&bh_date=03/03/2018'

        self.url3 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date='

        #A la urlBase habrá que añadirle las fechas que introduzca el usuario, la cadena YYYYYYY hay que sustituirla por el año de la fecha a tratar
        self.urlBase = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60000&screen_language=&bh_number=10&bh_year=YYYYYYY&bh_date='

        ###http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&
        # bh_number=10&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date=27/02/2018

        #Arrays de datos para el tratamiento de información
        self.coleccionURLdePartida = []
        self.coleccionURLconDatos = []

        #Las fechas las definimos a mano. En una versión posterior, será el usuario el que introduzca el periodo
        self.fechaIni = '2018-03-03'
        self.fechaFin = '2018-03-04'

    def cargarColeccionURLdePartida(self):

        ##El primer paso será cargar un array con un intervalo de fechas a partir de fecha inicio y fecha fin
        print("\n##############Comienza la carga de URL principales##############\n")

        fechas = [] #array de fechas con el formato necesario para la url
        fechasAux = np.arange(self.fechaIni, self.fechaFin, dtype='datetime64[D]') #generación de fechas como datetime64[D]

        for fecha in fechasAux:
            fecha_aux = pd.to_datetime(str(fecha))
            fechaFormateada = fecha_aux.strftime('%d/%m/%Y')
            fechas.append(fechaFormateada) #almacenamos la fecha con el formato adecuado para su posterior tratamiento

        ##Una vez que tenemos relleno el array de fechas, vamos generando las url "principales" y las almacenamos en un array
        for fecha in fechas:
            ts = pd.to_datetime(str(fecha))
            año = ts.strftime('%Y')
            auxUrlBase = self.urlBase.replace("YYYYYYY", año)+fecha
            print("Agregada URL para búsqueda: " + auxUrlBase)
            self.coleccionURLdePartida.append(auxUrlBase)

        print("\n##############Finalizada la carga de URL principales##############\n")

    def cargarURLconDatos(self):

        print("\n##############Comienza la carga de URL con datos##############\n")

        #Definimos esta url para concatenarle las direcciones que encontremos en cada página principal
        base_url = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?'

        for url in self.coleccionURLdePartida:


            html = urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find('table',
                              {"align": "center", "border": 0, "cellpadding": "1", "cellspacing": "1"})

            tr = table.find_all('tr')

            for i in range(0, len(tr)):

                # Inicialización para el bucle tr
                cols = tr[i].find_all('td')
                linea = []

                for n in range(0, len(cols)):
                    # print(n)
                    if n == 2:
                        # Aquí tenemos parte de la url que tendremos que usar
                        td_aux = cols[n]
                        link = td_aux.find('a').get('href')

                        #necesitamos quedarnos con la parte desde 'screen_code=60030' inclusive en adelante
                        #no encuentro la forma elegante de hacerlo, de momento queda así...
                        print(link)
                        link = link[-116:]
                        link = link.replace('+escape(,','')
                        link = link.replace(')', '')

                        print(link)
                        self.coleccionURLconDatos.append(link)

                        #base_url = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?'

            #             cabecera1.append(self.tratarTexto(td[n].text))
            #         elif i == 1:
            #             # Rellenar la cabecera2
            #             cabecera2.append(self.tratarTexto(td[n].text))
            #         else:
            #             # Rellenar datos de la fila
            #             linea.append(self.tratarTexto(td[n].text))
            #
            #     if i > 1:
            #         # Añadir fila a la matriz de filas
            #         datos = datos + [linea]
            #
            # # Obtener la zona hidrográfica
            # zona = self.tratarTexto(soup.find('td', {"class": "tdsubtitulo"}).text)

            # # Imprimimos la información obtenida de la url tratada
            # print(zona)
            # print(cabecera1)
            # print(cabecera2)
            # print(datos, '\n')

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
            texto = ''
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

        print(zona)
        print(cabecera1)
        print(cabecera2)
        print(datos)

    def scrape(self):

        #self.printInfoURL('http://eportal.mapama.gob.es/BoleHWeb/')
        self.tratarURL(self.url2)

    def cargaColeccionURL(self):
        #Aquí vendrá el código que nos permita recorrer las webs que queremos procesar

        #Cargamos las tres url de ejemplo que tenemos
        self.coleccionURL.append(self.url1)
        self.coleccionURL.append(self.url2)
        self.coleccionURL.append(self.url3)

    def tratarColeccionURL(self):

        for n in range(0, len(self.coleccionURL)):
            self.scrape(self.coleccionURL[n])