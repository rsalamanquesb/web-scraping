from scraper import ReservasHidraulicas
import argparse

#This is the main code document
#ejemplo de fechas: fechaInicio 2018-03-03 fechaFin 2018-04-04

print("Inicio \n")

#Introducción de fechas como argumentos
parser = argparse.ArgumentParser(description='Obtencion de informacion sobre embalses')
parser.add_argument('fechaInicio', metavar='fechaInicio', type=str, help='Introduzca fecha de inicio en formato YYYY-MM-DD')
parser.add_argument('fechaFin', metavar='fechaFin', type=str, help='Introduzca fecha de inicio en formato YYYY-MM-DD')

args = parser.parse_args()
print('Fecha inicio: '+args.fechaInicio)
print('Fecha fin: '+args.fechaFin)

#Se establece 1 segundo de espera
scraper = ReservasHidraulicas(args.fechaInicio, args.fechaFin, 1)
scraper.scrape()

print("\n Fin")