from scraper import ReservasHidraulicas

#This is the main code document

print("Inicio \n")

scraper = ReservasHidraulicas();

scraper.cargarColeccionURLdePartida();
scraper.cargarURLconDatos();

# scraper.scrape();

print("\n Fin")