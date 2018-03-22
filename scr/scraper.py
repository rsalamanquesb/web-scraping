from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
	'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Oriental&bh_amb_id=17&bh_date='
url2 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
	'bh_number=12&bh_year=2018&bh_amb_name=Cant%E1brico%20Occidental&bh_amb_id=12&bh_date='
url3 = 'http://eportal.mapama.gob.es/BoleHWeb/accion/cargador_pantalla.htm?screen_code=60030&screen_language=&' \
	'bh_number=12&bh_year=2018&bh_amb_name=Tajo&bh_amb_id=3&bh_date='


html = urlopen(url3).read()

cabecera1 = []
cabecera2 = []
datos = []

soup = BeautifulSoup(html, 'html.parser')

table = soup.find_all('table')

tr = table[14].find_all('tr')

for i in range (0, len(tr)):

	#Inicialización para el bucle tr
	td = tr[i].find_all('td')
	texto = ''
	linea = []

	for n in range (0, len(td)):
		if i == 0:
			#Rellenar la cabecera1
			texto = td[n].text.replace(u'\xa0','')
			texto = texto.replace('\n', '')
			texto = texto.replace('\t', '')
			texto = texto.replace(' ', '')
			cabecera1.append(texto)
		elif i == 1:
			# Rellenar la cabecera2
			texto = td[n].text.replace(u'\xa0','')
			texto = texto.replace('\n', '')
			texto = texto.replace('\t', '')
			texto = texto.replace(' ', '')
			cabecera2.append(texto)
		else:
			texto = td[n].text.replace(u'\xa0','')
			texto = texto.replace('\n', '')
			texto = texto.replace('\t', '')
			texto = texto.replace(' ', '')
			linea.append(texto)

	if i > 1:
		datos = datos + [linea]

print(cabecera1)
print(cabecera2)
print(datos)
