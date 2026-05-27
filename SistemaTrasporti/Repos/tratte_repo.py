import sys
import os

# serve per far funzionare questo file anche quando lo testo da solo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from Models.tratta import Tratta

class TratteRepository:
    # mi occupo di salvare e ripescare le tratte dei trasporti su un file csv
    
    def __init__(self, file_path: str = "tratte.csv"):
        # trovo la cartella principale del progetto e ci piazzo il file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self._file_path = os.path.join(base_dir, file_path)
        self._colonne = ["idTratta", "partenza", "arrivo", "orari", "prezzo"]

        # se il file non esiste lo creo al volo e ci scrivo solo l'intestazione
        if not os.path.exists(self._file_path):
            with open(self._file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self._colonne)

    def salva_tratta(self, tratta: Tratta) -> None:
        # impacchetto i dati della tratta in un dizionario
        dati = {
            "idTratta": str(tratta.get_id_tratta()),
            "partenza": tratta.get_partenza(),
            "arrivo": tratta.get_arrivo(),
            "orari": tratta.get_orari(),
            "prezzo": str(tratta.get_prezzo())
        }
        # apro il file in modalità 'a' (append) per aggiungere la riga in fondo senza cancellare il resto
        with open(self._file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._colonne)
            writer.writerow(dati)

    def ricerca_tratte(self, partenza: str = "", arrivo: str = "") -> list:
        tratte_trovate = []
        if not os.path.exists(self._file_path):
            return tratte_trovate

        with open(self._file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # faccio un controllo furbo: trasformo tutto in minuscolo così trovo la tratta anche se l'utente scrive "RoMa"
                match_partenza = (partenza.lower() in row["partenza"].lower()) if partenza else True
                match_arrivo = (arrivo.lower() in row["arrivo"].lower()) if arrivo else True

                # se la tratta corrisponde ai criteri di ricerca la ricreo come oggetto python e la metto in lista
                if match_partenza and match_arrivo:
                    tratta = Tratta(
                        id_tratta=int(row["idTratta"]),
                        partenza=row["partenza"],
                        arrivo=row["arrivo"],
                        orari=row["orari"],
                        prezzo=float(row["prezzo"])
                    )
                    tratte_trovate.append(tratta)
        return tratte_trovate


# area di test
if __name__ == "__main__":
    print("avvio i test per il repository delle tratte")
    
    # uso un file finto per evitare di scrivere dati sul database principale
    repo = TratteRepository("test_tratte.csv")
    
    tratta_prova = Tratta(99, "napoli", "firenze", "10:00 - 13:00", 35.00)
    
    print("salvo la tratta di prova")
    repo.salva_tratta(tratta_prova)
    
    print("cerco le tratte in partenza da napoli:")
    risultati = repo.ricerca_tratte(partenza="napoli")
    
    for r in risultati:
        print(r)
        
    print("test del repository concluso")