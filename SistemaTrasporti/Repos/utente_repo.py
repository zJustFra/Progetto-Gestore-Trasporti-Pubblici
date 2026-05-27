import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from Models.utente import Cliente, Amministratore, Controllore

class UtenteRepository:
    # gestisco il salvataggio e la ricerca degli utenti nel database csv
    
    def __init__(self, file_path: str = "utenti.csv"):
        # trovo la cartella base del progetto e imposto il file lì
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self._file_path = os.path.join(base_dir, file_path)
        self._colonne = ["email", "password", "nome", "cognome", "codiceFiscale", "livelloAccesso", "matricola", "ruolo"]

        # se il file non c'è lo creo vuoto e ci butto dentro gli account base per fare i test e poter loggare subito
        if not os.path.exists(self._file_path):
            with open(self._file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self._colonne)
            
            self.salva_utente(Cliente("mario.rossi@email.it", "Password123", "Mario", "Rossi", "RSSMRA80A01H501Z"))
            self.salva_utente(Controllore("controllore@sistema.it", "CtrlPass123", "Luigi", "Verdi", "MAT12345"))
            self.salva_utente(Amministratore("admin@sistema.it", "AdminPass123", "Anna", "Neri", 1))

    def salva_utente(self, utente) -> None:
        info = utente.getInfoUtilizzatore()
        with open(self._file_path, mode='a', newline='', encoding='utf-8') as f:
            # uso restval per riempire i buchi lasciati vuoti 
            writer = csv.DictWriter(f, fieldnames=self._colonne, restval='', extrasaction='ignore')
            writer.writerow(info)

    def trova_utente_per_email(self, email: str):
        if not os.path.exists(self._file_path):
            return None
            
        with open(self._file_path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"] == email:
                    # se trovo l'email guardo il ruolo e ricostruisco al volo l'oggetto corretto
                    ruolo = row.get("ruolo", "")
                    if ruolo == "Cliente":
                        return Cliente(row["email"], row["password"], row["nome"], row["cognome"], row["codiceFiscale"])
                    elif ruolo == "Controllore":
                        return Controllore(row["email"], row["password"], row["nome"], row["cognome"], row["matricola"])
                    elif ruolo == "Amministratore":
                        return Amministratore(row["email"], row["password"], row["nome"], row["cognome"], int(row["livelloAccesso"]) if row["livelloAccesso"] else 1)
        return None


# area di test
if __name__ == "__main__":
    print("avvio i test per il repository degli utenti")
    
    # uso un file finto per non intaccare il database vero e proprio
    repo = UtenteRepository("test_utenti.csv")
    
    nuovo_cliente = Cliente("test@mail.com", "passsegreta", "testnome", "testcognome", "CFTEST123")
    print("salvo un utente di prova nel file")
    repo.salva_utente(nuovo_cliente)
    
    print("provo a recuperare l'utente appena salvato")
    utente_ritrovato = repo.trova_utente_per_email("test@mail.com")
    
    if utente_ritrovato:
        print("utente recuperato con successo dal sistema")
        print("ruolo riconosciuto:", utente_ritrovato.getInfoUtilizzatore()["ruolo"])
        
    print("test del repository concluso")