import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import date
from Models.titoli import Biglietto, Carnet, Abbonamento
from Repos.titoli_repo import TitoliRepository

class GestoreTitoli:
    """Controller per l'acquisto, utilizzo e disdetta dei titoli di viaggio."""
    
    def __init__(self, repo=None):
        self._repo = repo if repo else TitoliRepository()

    def verifica_e_utilizza_titolo(self, codice: str) -> str:
        # vado a cercare il biglietto nel database usando il codice
        titolo = self._repo.ricerca_per_codice(codice)
        if not titolo:
            return "Errore: Titolo inesistente o contraffatto."
            
        if not titolo.isValido():
            return "Errore: Titolo non valido (scaduto, esaurito o già obliterato)."

        # se è un biglietto normale lo timbro, se è un carnet gli scalo un viaggio
        if isinstance(titolo, Biglietto):
            titolo.timbra()
        elif isinstance(titolo, Carnet):
            titolo.scalaViaggio()

        # mi ricordo di salvare la modifica nel file
        self._repo.salva(titolo)
        
        if isinstance(titolo, Carnet):
            return f"Titolo Valido! Viaggi residui: {titolo.get_viaggi_residui()}"
        return "Titolo Valido. Obliterazione confermata."

    def disdici_titolo(self, codice: str) -> bool:
        # tolgo le parentesi quadre e spezzo la stringa dove ci sono gli spazi
        lista_parole = codice.replace("[", "").replace("]", "").split(" ")
        
        # prendo solo il primo blocco che è il codice vero e proprio e tolgo gli spazi vuoti
        codice_pulito = lista_parole[0].strip()
        
        titolo = self._repo.ricerca_per_codice(codice_pulito)
        
        # se il biglietto esiste, è ancora valido e non l'ho già usato lo annullo
        if titolo and titolo.get_stato() == "Valido" and titolo.isValido():
            titolo.setStato("Annullato")
            self._repo.salva(titolo)
            return True
            
        return False

    def creaTitoloViaggio(self, tratta: str, email: str, tipo="Biglietto", data_inizio=None, durata=None) -> bool:
        # preparo il codice iniziale e gli attacco un numero a caso
        prefisso = "BIGL" if tipo == "Biglietto" else "CARN" if tipo == "Carnet" else "ABBN"
        codice = f"{prefisso}-{random.randint(1000, 9999)}"

        if tipo == "Biglietto":
            nuovo_titolo = Biglietto(codice, 2.50)
        elif tipo == "Carnet":
            nuovo_titolo = Carnet(codice, 20.00, 10)
        else:
            if not data_inizio:
                data_inizio = date.today().strftime("%d/%m/%Y")
                
            durata_giorni = durata if durata else 30
            
            # imposto il prezzo fisso in base a quanti giorni dura l'abbonamento
            if durata_giorni == 7:
                prezzo = 15.00
            elif durata_giorni == 30:
                prezzo = 50.00
            else:
                prezzo = 400.00
                
            nuovo_titolo = Abbonamento(codice, prezzo, data_inizio, durata_giorni)

        # salvo la stringa della tratta dentro l'oggetto così poi la posso stampare a schermo
        nuovo_titolo._tratta = tratta

        self._repo.salva(nuovo_titolo, email)
        return True

    def ricerca_titoli_utente(self, email: str) -> list:
        return self._repo.ricerca_titoli_utente(email)


# area di test
if __name__ == "__main__":
    print("avvio il test per il gestore dei titoli")
    
    # creo un gestore appoggiandomi a un file di test per non fare casini
    repo_test = TitoliRepository("test_titoli_gestore.csv")
    gestore = GestoreTitoli(repo_test)
    
    print("provo a comprare un biglietto singolo")
    gestore.creaTitoloViaggio("roma-milano", "mario@mail.it", "Biglietto")
    
    titoli = gestore.ricerca_titoli_utente("mario@mail.it")
    print("titoli comprati:")
    for t in titoli:
        print(t)
        
    print("test del gestore titoli concluso")