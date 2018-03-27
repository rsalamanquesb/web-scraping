from scraper import ReservasHidraulicas

#This is the main code document

print("Inicio \n")

scraper = ReservasHidraulicas();

scraper.cargarColeccionURLdePartida();

#scraper.scrape();
#scraper.cargaColeccionURL();
#scraper.tratarColeccionURL();

print("\n Fin")