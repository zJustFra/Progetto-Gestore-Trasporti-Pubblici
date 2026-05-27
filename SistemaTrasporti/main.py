import sys
from PyQt6.QtWidgets import QApplication
from Controllers.gestore_utenza import GestoreUtenza
from Controllers.gestore_tratte import GestoreTratte
from Controllers.gestore_titoli import GestoreTitoli
from Controllers.gestore_backup import GestoreBackup
from Views.vista_utenza import VistaUtenza
from Views.vista_acquisti import VistaAcquisti
from Views.vista_area_personale import VistaAreaPersonale
from Views.vista_controllore import VistaControllore
from Views.vista_amministratore import VistaAmministratore
import threading
import time

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # preparo tutti i gestori della logica che mi servono per far funzionare l'applicazione
        self.gestore_utenza = GestoreUtenza()
        self.gestore_tratte = GestoreTratte()
        self.gestore_titoli = GestoreTitoli()
        self.gestore_backup = GestoreBackup()
        
        # faccio partire un processo invisibile in background per gestire i salvataggi automatici (RF14)
        threading.Thread(target=self.loop_tempo, daemon=True).start()

    def loop_tempo(self):
        """Simula l'attore Tempo che ogni giorno fa il backup dei dati."""
        while True:
            # metto in pausa per sessanta secondi e poi lancio la copia dei file
            time.sleep(60) 
            self.gestore_backup.effettuaBackup()

    def avvia(self):
        # apro la schermata iniziale di accesso e dico al sistema di far partire l'interfaccia grafica
        self.vista_login = VistaUtenza(self.gestore_utenza)
        self.vista_login.on_login_completato = self.smista_utente
        self.vista_login.show()
        sys.exit(self.app.exec())

    def smista_utente(self, utente_loggato):
        # appena qualcuno fa l'accesso chiudo il login e guardo il suo ruolo per aprirgli le schermate corrette
        self.vista_login.close()
        ruolo = type(utente_loggato).__name__

        if ruolo == "Cliente":
            # se è un cliente gli apro sia il negozio dei biglietti sia la sua area personale
            self.v1 = VistaAcquisti(self.gestore_tratte, self.gestore_titoli, utente_loggato)
            self.v2 = VistaAreaPersonale(self.gestore_titoli, utente_loggato)
            self.v1.show()
            self.v2.show()
        elif ruolo == "Controllore":
            self.v = VistaControllore(self.gestore_titoli)
            self.v.show()
        elif ruolo == "Amministratore":
            self.v = VistaAmministratore(self.gestore_tratte)
            self.v.show()

# area di avvio
if __name__ == "__main__":
    print("faccio partire il programma principale del gestore trasporti")
    app = MainApp()
    app.avvia()