# Práctica 1: Web scraping

## Descripción

Práctica desarrollada para la asignatura _Tipología y ciclo de vida de los datos_, dentro del Máster en Ciencia de Datos de la Universitat Oberta de Catalunya (UOC). Se aplicarán técnicas de _web scraping_ utilizando el lenguaje  Python para obtener información contenida en la web _XXXXXXXXXX_ y generar un _dataset_ con datos que puedan ser utilizados posteriormente en un proyecto de minería de datos.

## Miembros del equipo

**Rubén Salamanqués Ballesteros**
**Ricardo Pardo Calvo**

## Ficheros del código fuente

* **src/main.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **src/scraper.py**: contiene la implementación de la clase _AccidentsScraper_ cuyos métodos generan el conjunto de datos a partir de la base de datos online [PlaneCrashInfo](http://www.planecrashinfo.com/database.htm).
* **src/reason_classifier.py**: contiene la implementación de la clase que se encarga de asignar una causa a un resumen de accidente dado. Para ello, utiliza la librería *TextBlob*.

## Recursos

Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.
Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
Tutorial de Github https://guides.github.com/activities/hello-world
