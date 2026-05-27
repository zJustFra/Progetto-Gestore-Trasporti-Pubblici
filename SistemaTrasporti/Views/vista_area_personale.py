import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QMessageBox

class VistaAreaPersonale(QWidget):
    def __init__(self, gestore_titoli, utente):
        super().__init__()
        # mi salvo il gestore dei titoli e tiro fuori l'email dell'utente per sapere a chi appartengono i biglietti
        self._gestore_titoli = gestore_titoli
        dati = utente.getInfoUtilizzatore() if hasattr(utente, 'getInfoUtilizzatore') else {}
        self._email = dati.get('email', '')
        
        self.setWindowTitle("I Miei Titoli")
        self.resize(350, 300)
        layout = QVBoxLayout()
        
        self.lista = QListWidget()
        btn_agg = QPushButton("🔄 Aggiorna Lista")
        btn_agg.clicked.connect(self.carica)
        
        btn_disdici = QPushButton("Disdici Selezionato (Rimborso 50%)")
        # coloro il bottone di rosso e lo metto in grassetto per far capire all'utente che fa un'azione irreversibile
        btn_disdici.setStyleSheet("color: red; font-weight: bold;")
        btn_disdici.clicked.connect(self.disdici)
        
        layout.addWidget(btn_agg)
        layout.addWidget(self.lista)
        layout.addWidget(btn_disdici)
        self.setLayout(layout)
        
        # appena apro la finestra chiamo subito il caricamento per non farla apparire vuota
        self.carica()

    def carica(self):
        # pulisco la schermata e chiedo al gestore di darmi tutti gli acquisti fatti con questa email
        self.lista.clear()
        titoli = self._gestore_titoli.ricerca_titoli_utente(self._email)
        self.lista.addItems(titoli if titoli else ["Nessun acquisto trovato."])

    def disdici(self):
        # controllo quale riga ha selezionato e fermo tutto se ha cliccato sul messaggio di lista vuota
        item = self.lista.currentItem()
        if not item or "Nessun" in item.text():
            return
            
        # passo il testo della riga al gestore che si occuperà di estrarre il codice e annullare il biglietto
        if self._gestore_titoli.disdici_titolo(item.text()):
            QMessageBox.information(self, "Ok", "Rimborso emesso.")
            # ricarico la lista così il titolo appena annullato si aggiorna subito a schermo
            self.carica()
        else:
            QMessageBox.warning(self, "Errore", "Impossibile disdire questo titolo.")


# area di test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    print("avvio il test per l'area personale")
    
    # preparo i finti oggetti per far partire la grafica isolata dal resto del programma
    class FintoGestoreTitoli:
        def ricerca_titoli_utente(self, email):
            return ["[BIGL-1234] - Biglietto - roma-milano (Valido)", "[CARN-9999] - Carnet - napoli-bari (Valido)"]
            
        def disdici_titolo(self, codice):
            print("simulo l'annullamento del titolo con codice:", codice)
            return True
            
    class FintoUtente:
        def getInfoUtilizzatore(self):
            return {"email": "cliente@mail.it"}
            
    app = QApplication(sys.argv)
    finestra_prova = VistaAreaPersonale(FintoGestoreTitoli(), FintoUtente())
    finestra_prova.show()
    sys.exit(app.exec())