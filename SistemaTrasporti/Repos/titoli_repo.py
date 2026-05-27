import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.titoli import Biglietto, Carnet, Abbonamento

class TitoliRepository:
    # gestisco il salvataggio e il recupero dei biglietti su un file csv
    def __init__(self, file_path: str = "titoli.csv"):
        # trovo la cartella principale del progetto e ci piazzo il file
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self._file_path = os.path.join(base_dir, file_path)
        
        # definisco le colonne del file
        self._campi = ["codice", "tipo", "stato", "prezzo", "extra", "email", "tratta"]
        
        # se il file non c'è lo creo e ci scrivo l'intestazione
        if not os.path.exists(self._file_path):
            with open(self._file_path, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self._campi)
                writer.writeheader()

    def salva(self, titolo, email=""):
        tipo = type(titolo).__name__
        extra = ""
        
        # in base al tipo di biglietto, mi salvo dei dati "extra" più specifici
        if tipo == "Carnet":
            extra = str(titolo.get_viaggi_residui())
        elif tipo == "Abbonamento":
            extra = f"{titolo._dataInizio}|{titolo._durataGiorni}"
        
        nuova_riga = {
            "codice": titolo.get_codice(),
            "tipo": tipo,
            "stato": titolo.get_stato(),
            "prezzo": str(titolo.get_prezzo()),
            "extra": extra,
            "email": email,
            "tratta": getattr(titolo, '_tratta', "") 
        }
        
        righe = []
        trovato = False
        
        if os.path.exists(self._file_path):
            with open(self._file_path, mode="r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                righe = list(reader)
            
            # cerco se il titolo esiste già nel file per aggiornarlo
            for riga in righe:
                if riga["codice"] == titolo.get_codice():
                    if email == "":
                        # se aggiorno solo lo stato non vado a sovrascrivere l'email e la tratta
                        nuova_riga["email"] = riga.get("email", "")
                        nuova_riga["tratta"] = riga.get("tratta", "")
                    riga.update(nuova_riga)
                    trovato = True
                    break
        
        # se non l'ho trovato lo aggiungo in fondo
        if not trovato:
            righe.append(nuova_riga)
            
        # riscrivo tutto il file aggiornato
        with open(self._file_path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self._campi)
            writer.writeheader()
            writer.writerows(righe)

    def ricerca_per_codice(self, codice):
        if not os.path.exists(self._file_path):
            return None
        with open(self._file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["codice"] == codice:
                    # se lo trovo lo trasformo di nuovo in un oggetto python
                    return self._ricostruisci_oggetto(row)
        return None

    def ricerca_titoli_utente(self, email):
        titoli_utente = []
        if not os.path.exists(self._file_path):
            return titoli_utente
        with open(self._file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("email") == email:
                    titolo = self._ricostruisci_oggetto(row)
                    if titolo:
                        # preparo la stringa formattata come si deve da far vedere a schermo
                        tratta_info = row.get("tratta", "Tratta N/D")
                        titoli_utente.append(f"[{titolo.get_codice()}] - {row['tipo']} - {tratta_info} ({titolo.get_stato()})")
        return titoli_utente

    def _ricostruisci_oggetto(self, row):
        # prendo i dati dal csv e ricreo l'oggetto giusto in base al tipo
        codice = row["codice"]
        tipo = row["tipo"]
        stato = row["stato"]
        prezzo = float(row["prezzo"])
        extra = row.get("extra", "")
        
        titolo = None
        if tipo == "Biglietto":
            titolo = Biglietto(codice, prezzo)
            if stato != "Valido":
                titolo.timbra()
        elif tipo == "Carnet":
            viaggi = int(extra) if extra else 0
            titolo = Carnet(codice, prezzo, viaggi)
        elif tipo == "Abbonamento":
            if "|" in extra:
                data_inizio, durata = extra.split("|")
                titolo = Abbonamento(codice, prezzo, data_inizio, int(durata))
            else:
                titolo = Abbonamento(codice, prezzo, "01/01/2026", 30)
        
        if titolo:
            titolo.setStato(stato)
            titolo._tratta = row.get("tratta", "")
        return titolo


# area di test
if __name__ == "__main__":
    print("avvio i test per il repository dei titoli di viaggio")
    
    # uso un file di test per evitare di "sporcare" il database vero
    repo = TitoliRepository("test_titoli.csv")
    
    biglietto_prova = Biglietto("TEST-1234", 2.50)
    biglietto_prova._tratta = "roma-napoli"
    
    print("salvo il biglietto di prova")
    repo.salva(biglietto_prova, "utente@test.it")
    
    ritrovato = repo.ricerca_per_codice("TEST-1234")
    if ritrovato:
        print("biglietto recuperato con successo dal file")
        
    lista_titoli = repo.ricerca_titoli_utente("utente@test.it")
    print("titoli trovati per questo utente:")
    for t in lista_titoli:
        print(t)
        
    print("test del repository concluso")