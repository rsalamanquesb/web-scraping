from bs4 import BeautifulSoup
from urllib.request import urlopen

class ReservasHidraulicas:

    def __init__(self):
        self.url = ['2018', '12', 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date=']
        self.url2 = ['2018', '12', 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date=']
        self.url3 = ['2018', '12', 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date=']
        self.datos = []

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
            embalse = texto[1:] #Se quita el asterisco
            embalse = embalse.strip() #Se eliminan los espacios que existían entre el asterisco y el nombre

        return tipo, embalse

    def tratarURL(self, url):

        #url es una matriz con [año, semana, link]
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
                        #Se rellenan columnas propias no presentes en la tabla
                        cabecera.append("Anyo")
                        cabecera.append("Semana")
                        cabecera.append("Zona Hidrográfica")
                        cabecera.append("Embalse Hidroeléctrico")

                    # Rellenar la cabecera1 con la primera fila
                    cabecera.append(self.tratarTexto(td[n].text))

                elif i == 1:
                    # Rellenar la cabecera1 con la segunda fila
                    # Se concatena con el título superior
                    if n in (0,1,2):
                        cabecera.append(cabecera[6]+" "+self.tratarTexto(td[n].text))
                    elif n in (3,4):
                        cabecera.append(cabecera[7]+" "+self.tratarTexto(td[n].text))
                else:
                    #Cada 10 lineas la página pinta una vacía para facilitar la legibilidad
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

            #Si todavía no hay datos guardados y hemos guardado ya las cabeceras
            if len(self.datos) == 0 and i == 1:
                #Se eliminan los elementos innecesarios de la cabecera
                cabecera.pop(6)
                cabecera.pop(6)
                #Se guarda la cabecera
                self.datos = self.datos + [cabecera]

            #Si es una linea de datos y no está vacía
            if i > 1 and len(linea)>0:
                # Añadir fila a la matriz de filas
                self.datos = self.datos + [linea]

        print(len(self.datos))

    def exportarCSV(self, fichero):
        file = open("../csv/"+fichero, "w+")

        for linea in range(len(self.datos)):
            for dato in range (len(self.datos[linea])):
                file.write(self.datos[linea][dato]+";") #Nuevo dato
            file.write("\n")#Nueva línea

    def scrape(self):
        self.tratarURL(self.url)
        self.tratarURL(self.url2)
        self.tratarURL(self.url3)
        print(self.datos)
        self.exportarCSV("prueba.csv")