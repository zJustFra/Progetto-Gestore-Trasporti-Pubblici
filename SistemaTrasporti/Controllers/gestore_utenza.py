import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.utente import Cliente
from Repos.utente_repo import UtenteRepository

class GestoreUtenza:
    """Controller per la gestione degli utenti (Registrazione, Login)."""
    
    def __init__(self, repo=None):
        # mi collego al database degli utenti, se non mi viene passato niente uso quello di default
        self._repo = repo if repo else UtenteRepository()

    def registra_cliente(self, nome: str, cognome: str, cf: str, email: str, password: str) -> bool:
        # prima di tutto blocco chi prova a usare una password troppo corta
        if len(password) < 8:
            return False
            
        # controllo se c'è già uno registrato con la stessa email
        if self._repo.trova_utente_per_email(email) is not None:
            return False
            
        # tutto ok, creo il cliente nuovo e lo metto dentro al file csv
        nuovo_cliente = Cliente(email, password, nome, cognome, cf)
        self._repo.salva_utente(nuovo_cliente)
        return True

    def effettua_login(self, email: str, password: str):
        # vado a pescare l'utente dal file tramite la sua email
        utente = self._repo.trova_utente_per_email(email)
        
        # tiro fuori i suoi dati e guardo se la password inserita coincide con la sua
        if utente is None or utente.getInfoUtilizzatore()["password"] != password:
            return None
        return utente


# area di test
if __name__ == "__main__":
    print("avvio il test per il gestore utenza")
    
    # creo un repo di prova per non sporcare i dati veri
    repo_test = UtenteRepository("test_utenza_gestore.csv")
    gestore = GestoreUtenza(repo_test)
    
    print("provo a registrare un cliente nuovo")
    esito_reg = gestore.registra_cliente("mario", "rossi", "MRARSS99", "mario@mail.it", "password123")
    
    if esito_reg:
        print("registrazione andata a buon fine")
    else:
        print("errore durante la registrazione controlla password o email")
        
    print("provo a fare il login con i dati appena inseriti")
    utente_loggato = gestore.effettua_login("mario@mail.it", "password123")
    
    if utente_loggato:
        print("login effettuato con successo bentornato", utente_loggato.getInfoUtilizzatore()["nome"])
    else:
        print("credenziali errate o utente non trovato")
        
    print("test del gestore utenza concluso")