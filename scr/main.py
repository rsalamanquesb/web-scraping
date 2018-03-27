from scraper import ReservasHidraulicas

#This is the main code document

print("Inicio \n")

scraper = ReservasHidraulicas();
#scraper.scrape();
#scraper.cargarArrayFechas();
scraper.cargarColeccionURLdePartida();
#scraper.cargaColeccionURL();
#scraper.tratarColeccionURL();

print("\n Fin")