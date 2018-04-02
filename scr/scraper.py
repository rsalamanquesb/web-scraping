from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd
import re


class ReservasHidraulicas:

    def __init__(self):

        # A la urlBase habrá que añadirle la semana y el año
        self.urlBase = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60000&screen_language=&bh_number=WEEK&bh_year=YEAR'

        # Arrays de datos para el tratamiento de información
        self.coleccionURLdePartida = ([])  # contendrá listas con el formato: [año, semana, urlPrincipal]
        self.coleccionURLconDatos = ([])  # contendrá listas con el formato: [año, semana, urlConDatos]
        self.datos = []

        # Las fechas las definimos a mano. En una versión posterior, será el usuario el que introduzca el periodo
        self.fechaIni = '2018-02-18'
        self.fechaFin = '2018-03-05'

    def cargarColeccionURLdePartida(self):

        ##El primer paso será cargar un array con un intervalo de fechas a partir de fecha inicio y fecha fin
        print("\n##############Comienza la carga de URL principales##############\n")

        # fechas = [] #array de fechas con el formato necesario para la url
        semanas = ([])  # lista de duplas semana-año para generar las url necesarias
        fechasAux = np.arange(self.fechaIni, self.fechaFin,
                              dtype='datetime64[D]')  # generación de fechas como datetime64[D]

        # Obtenemos las diferentes semanas dentro del intervalo de fechas que nos han introducido
        for fecha in fechasAux:
            fecha_aux = pd.to_datetime(str(fecha))
            anio = fecha_aux.isocalendar()[0]  # obtenemos el año de la fecha introducida
            sem = fecha_aux.isocalendar()[1]  # obtenemos la semana de la fecha introducida
            # fechaFormateada = fecha_aux.strftime('%d/%m/%Y')
            # fechas.append(fechaFormateada) #almacenamos la fecha con el formato adecuado para su posterior tratamiento

            # agregamos año-semana a la lista
            if ([anio, sem]) not in semanas:
                semanas.append([anio, sem])

        # Una vez que tenemos relleno el array de fechas, vamos generando las url "principales" y las almacenamos en la lista definida en self
        for sem in semanas:
            anio = str(sem[0])
            sem = str(sem[1])
            auxUrlBase = self.urlBase
            auxUrlBase = auxUrlBase.replace("YEAR", anio)
            auxUrlBase = auxUrlBase.replace("WEEK", sem)

            self.coleccionURLdePartida.append([anio, sem, auxUrlBase])
            print("Agregada URL principal para búsqueda: " + anio + "-" + sem + " -> " + auxUrlBase)

        print("\n##############Finalizada la carga de URL principales##############\n")

    def cargarURLconDatos(self):

        print("\n##############Comienza la carga de URL con datos##############\n")

        # Definimos esta url para concatenarle las direcciones que encontremos en cada página principal
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

                        # Con esta comprobación descartamos el primer link, que corresponde a los datos generales de la península
                        if 'name' in html:
                            # Llevamos a cabo una limpieza "manual" de los links
                            html = html.replace(' ', '')
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
                            print("Agregada URL con datos para búsqueda: " + anio + "-" + sem + " -> " + urlDatos)

        print("\n##############Finalizada la carga de URL con datos##############\n")

    def tratarTexto(self, texto):

        texto = texto.replace(u'\xa0', '')
        texto = texto.replace('\n', ' ')
        texto = texto.replace('\t', ' ')
        texto = texto.strip()

        return texto

    def tratarEmbalse(self, texto):

        tipo = "NO"
        embalse = texto
        primeraletra = texto[0]

        if primeraletra == "*":
            tipo = "SI"
            embalse = texto[1:]  # Se quita el asterisco
            embalse = embalse.strip()  # Se eliminan los espacios que existían entre el asterisco y el nombre

        return tipo, embalse

    def tratarURL(self, url):

        # url es una matriz con [año, semana, link]
        anyo = str(url[0])
        semana = str(url[1])
        html = urlopen(url[2]).read()

        cabecera = []

        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table',
                          {"width": "90%", "cellspacing": "1", "cellpadding": "1", "border": 0, "align": "center"})

        tr = table.find_all('tr')

        # Obtener la zona hidrográfica
        zona = self.tratarTexto(soup.find('td', {"class": "tdsubtitulo"}).text)
        for i in range(0, len(tr)):

            # Inicialización para el bucle tr
            td = tr[i].find_all('td')
            linea = []

            for n in range(0, len(td)):
                if i == 0:
                    if n == 0:
                        # Se rellenan columnas propias no presentes en la tabla
                        cabecera.append("Anyo")
                        cabecera.append("Semana")
                        cabecera.append("Zona Hidrográfica")
                        cabecera.append("Embalse Hidroeléctrico")

                    # Rellenar la cabecera1 con la primera fila
                    cabecera.append(self.tratarTexto(td[n].text))

                elif i == 1:
                    # Rellenar la cabecera1 con la segunda fila
                    # Se concatena con el título superior
                    if n in (0, 1, 2):
                        cabecera.append(cabecera[6] + " " + self.tratarTexto(td[n].text))
                    elif n in (3, 4):
                        cabecera.append(cabecera[7] + " " + self.tratarTexto(td[n].text))
                else:
                    # Cada 10 lineas la página pinta una vacía para facilitar la legibilidad
                    if len(self.tratarTexto(td[n].text)) > 0:

                        # En el dato de la primera columna se obtiene si el embalse
                        # es o no hidroeléctrico
                        if n == 0:
                            linea.append(anyo)
                            linea.append(semana)
                            linea.append(zona)

                            tipo, embalse = self.tratarEmbalse(self.tratarTexto(td[n].text))
                            # Rellenar datos de la fila
                            linea.append(tipo)
                            linea.append(embalse)

                        elif n > 0:
                            # Rellenar datos de la fila
                            linea.append(self.tratarTexto(td[n].text))

            # Si todavía no hay datos guardados y hemos guardado ya las cabeceras
            if len(self.datos) == 0 and i == 1:
                # Se eliminan los elementos innecesarios de la cabecera
                cabecera.pop(6)
                cabecera.pop(6)
                # Se guarda la cabecera
                self.datos = self.datos + [cabecera]

            # Si es una linea de datos y no está vacía
            if i > 1 and len(linea) > 0:
                # Añadir fila a la matriz de filas
                self.datos = self.datos + [linea]

        print(len(self.datos))

    def exportarCSV(self, fichero):
        file = open("../csv/" + fichero, "w+")

        for linea in range(len(self.datos)):
            for dato in range(len(self.datos[linea])):
                file.write(self.datos[linea][dato] + ";")  # Nuevo dato
            file.write("\n")  # Nueva línea

    def scrape(self):
        self.cargarColeccionURLdePartida()
        self.cargarURLconDatos()

        for i in range(0, len(self.coleccionURLconDatos)):
            self.tratarURL(self.coleccionURLconDatos[i])

        self.exportarCSV("prueba.csv")
