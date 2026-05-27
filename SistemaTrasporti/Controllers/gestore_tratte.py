import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Repos.tratte_repo import TratteRepository
from Models.tratta import Tratta

class GestoreTratte:
    """Controller che coordina la ricerca e l'aggiunta delle tratte di trasporto."""
    
    def __init__(self, repo=None):
        # mi aggancio al repository delle tratte per potergli passare o chiedere i dati
        self._repo = repo if repo else TratteRepository()

    def aggiungi_tratta(self, partenza: str, arrivo: str, orari: str, prezzo: float):
        # prima di fare qualsiasi cosa controllo se c'è già una tratta identica
        if self._repo.ricerca_tratte(partenza, arrivo):
            return "Errore: Tratta già presente nel sistema."
            
        # mi tiro giù tutte le tratte per capire quale id assegnare a quella nuova
        tutte_le_tratte = self._repo.ricerca_tratte()
        nuovo_id = max([t.get_id_tratta() for t in tutte_le_tratte]) + 1 if tutte_le_tratte else 1
            
        # creo la tratta con l'id calcolato e la salvo direttamente nel database
        nuova_tratta = Tratta(nuovo_id, partenza, arrivo, orari, prezzo)
        self._repo.salva_tratta(nuova_tratta)
        return nuova_tratta

    def ricerca_tratta(self, partenza: str = "", arrivo: str = "") -> list:
        # giro semplicemente la richiesta al repository che fa il lavoro di ricerca per me
        return self._repo.ricerca_tratte(partenza, arrivo)


# area di test
if __name__ == "__main__":
    print("avvio il test per il gestore delle tratte")
    
    # uso un repo su un file temporaneo per non intaccare quello ufficiale
    repo_test = TratteRepository("test_tratte_gestore.csv")
    gestore = GestoreTratte(repo_test)
    
    print("provo ad aggiungere una tratta nuova")
    esito = gestore.aggiungi_tratta("torino", "venezia", "09:00 - 14:00", 25.50)
    
    if isinstance(esito, str):
        print("il sistema mi ha bloccato dicendo:", esito)
    else:
        print("tratta aggiunta correttamente con id:", esito.get_id_tratta())
        
    print("provo a cercare la tratta appena inserita")
    ricerca = gestore.ricerca_tratta("torino", "venezia")
    for r in ricerca:
        print(r)
        
    print("test del gestore tratte concluso")