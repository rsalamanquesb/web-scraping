from bs4 import BeautifulSoup
from urllib.request import urlopen

from ipwhois import IPWhois

class ReservasHidraulicas:

    def __init__(self):
        self.url1 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date='
        self.url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date='
        self.url3 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
            'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date='
        self.coleccionURL = []

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