from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd
import re

class ReservasHidraulicas:

    def __init__(self):

        self.url1 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date='
        self.url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date='
        self.url3 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date='

        #A la urlBase habrá que añadirle la semana y el año
        self.urlBase = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60000&screen_language=&bh_number=WEEK&bh_year=YEAR'

        #Arrays de datos para el tratamiento de información
        self.coleccionURLdePartida = ([]) #contendrá listas con el formato: [año, semana, urlPrincipal]
        self.coleccionURLconDatos = ([]) #contendrá listas con el formato: [año, semana, urlConDatos]

        #Las fechas las definimos a mano. En una versión posterior, será el usuario el que introduzca el periodo
        self.fechaIni = '2018-02-18'
        self.fechaFin = '2018-03-05'

    def cargarColeccionURLdePartida(self):

        ##El primer paso será cargar un array con un intervalo de fechas a partir de fecha inicio y fecha fin
        print("\n##############Comienza la carga de URL principales##############\n")

        # fechas = [] #array de fechas con el formato necesario para la url
        semanas = ([])  # lista de duplas semana-año para generar las url necesarias
        fechasAux = np.arange(self.fechaIni, self.fechaFin, dtype='datetime64[D]') #generación de fechas como datetime64[D]

        #Obtenemos las diferentes semanas dentro del intervalo de fechas que nos han introducido
        for fecha in fechasAux:
            fecha_aux = pd.to_datetime(str(fecha))
            anio = fecha_aux.isocalendar()[0]  # obtenemos el año de la fecha introducida
            sem = fecha_aux.isocalendar()[1] #obtenemos la semana de la fecha introducida
            # fechaFormateada = fecha_aux.strftime('%d/%m/%Y')
            # fechas.append(fechaFormateada) #almacenamos la fecha con el formato adecuado para su posterior tratamiento

            # agregamos año-semana a la lista
            if ([anio,sem]) not in semanas:
                semanas.append([anio,sem])

        #Una vez que tenemos relleno el array de fechas, vamos generando las url "principales" y las almacenamos en la lista definida en self
        for sem in semanas:
            anio = sem[0]
            sem = sem[1]
            auxUrlBase = self.urlBase
            auxUrlBase = auxUrlBase.replace("YEAR", str(anio))
            auxUrlBase = auxUrlBase.replace("WEEK", str(sem))

            self.coleccionURLdePartida.append([anio, sem, auxUrlBase])
            print("Agregada URL principal para búsqueda: " + str(anio) + "-" + str(sem) + " -> " + auxUrlBase)

        print("\n##############Finalizada la carga de URL principales##############\n")

    def cargarURLconDatos(self):

        print("\n##############Comienza la carga de URL con datos##############\n")

        #Definimos esta url para concatenarle las direcciones que encontremos en cada página principal
        url_parte_comun = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?'

        for tupla in self.coleccionURLdePartida:

            anio = tupla[0]
            sem = tupla[1]
            url = tupla[2]

            html = urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')

            table = soup.find('table',
                              {"align": "center", "border": 0, "cellpadding": "1", "cellspacing": "1"})

            tr = table.find_all('tr')

            for i in range(0, len(tr)):

                # Inicialización para el bucle tr
                cols = tr[i].find_all('td')

                for n in range(0, len(cols)):
                    # print(n)
                    if n == 2:
                        # Aquí tenemos parte de la url que tendremos que usar
                        td_aux = cols[n]
                        html = td_aux.find('a').get('href')

                        #Con esta comprobación descartamos el primer link, que corresponde a los datos generales de la península
                        if 'name' in html:
                            #Llevamos a cabo una limpieza "manual" de los links
                            html = html.replace(' ','')
                            html = html.replace('\r\n', '')
                            html = html.replace('javascript:window.location.href=', '')
                            html = html.replace('/BoleHWeb/accion/cargador_pantalla.htm;', '')
                            html = html[45:]
                            html = re.sub('[^a-zA-Z0-9\n\._&=/ñ]', '', html)
                            html = html.replace('=escape', '=')
                            html = html.replace('ñ', 'ny')
                            html = html[:-9]
                            urlDatos = url_parte_comun + html

                            self.coleccionURLconDatos.append([anio, sem, urlDatos])
                            print("Agregada URL con datos para búsqueda: " + str(anio) + "-" + str(sem) + " -> " + urlDatos)

        print("\n##############Finalizada la carga de URL con datos##############\n")

    def tratarTexto(self, texto):

        texto = texto.replace(u'\xa0', '')
        texto = texto.replace('\n', ' ')
        texto = texto.replace('\t', ' ')
        texto = texto.strip()

        return texto

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
        #self.tratarURL(self.url2)
        self.cargarColeccionURLdePartida();
        self.cargarURLconDatos();

    def cargaColeccionURL(self):
        #Aquí vendrá el código que nos permita recorrer las webs que queremos procesar

        #Cargamos las tres url de ejemplo que tenemos
        self.coleccionURL.append(self.url1)
        self.coleccionURL.append(self.url2)
        self.coleccionURL.append(self.url3)

    def tratarColeccionURL(self):

        for n in range(0, len(self.coleccionURL)):
            self.scrape(self.coleccionURL[n])