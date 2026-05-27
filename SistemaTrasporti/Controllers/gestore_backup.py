import os
import shutil
from datetime import datetime

class GestoreBackup:
    """Controller che gestisce il salvataggio di sicurezza dei dati (RF14)."""

    def __init__(self):
        # mi trovo la cartella base del progetto e imposto dove andranno a finire i salvataggi
        self._base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self._backup_dir = os.path.join(self._base_dir, "Backups")
        
        # se la cartella generale per i backup non c'è la creo sul momento
        if not os.path.exists(self._backup_dir):
            os.makedirs(self._backup_dir, exist_ok=True)

    def effettuaBackup(self) -> bool:
        # prendo la data e l'ora esatta per dare un nome univoco alla cartella di questo salvataggio
        data_odierna = datetime.now().strftime("%Y-%m-%d_%H-%M")
        cartella_odierna = os.path.join(self._backup_dir, f"Backup_{data_odierna}")

        if not os.path.exists(cartella_odierna):
            os.makedirs(cartella_odierna, exist_ok=True)

        files_da_salvare = ["utenti.csv", "tratte.csv", "titoli.csv"]

        try:
            # prendo i file da salvare e ne faccio una copia identica nella cartella nuova
            for file_name in files_da_salvare:
                percorso_origine = os.path.join(self._base_dir, file_name)
                percorso_destinazione = os.path.join(cartella_odierna, file_name)
                
                # copio il file solo se esiste davvero nel sistema
                if os.path.exists(percorso_origine):
                    shutil.copy(percorso_origine, percorso_destinazione)
            return True
        except Exception:
            # se esplode qualcosa durante la copia fermo tutto e segnalo che è andata male
            return False


# area di test
if __name__ == "__main__":
    print("avvio il test per il gestore dei backup")
    
    gestore = GestoreBackup()
    esito = gestore.effettuaBackup()
    
    if esito:
        print("salvataggio completato con successo controlla la cartella Backups")
    else:
        print("si è verificato un problema durante la copia dei file")
        
    print("test del gestore backup concluso")