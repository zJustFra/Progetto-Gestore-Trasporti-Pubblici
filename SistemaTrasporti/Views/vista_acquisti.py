import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QDateEdit, QComboBox
from PyQt6.QtCore import QDate, QTimer

class VistaAcquisti(QWidget):
    def __init__(self, gestore_tratte, gestore_titoli, utente):
        super().__init__()
        # mi salvo i gestori e recupero subito l'email dell'utente connesso
        self._gestore_tratte = gestore_tratte
        self._gestore_titoli = gestore_titoli
        
        dati = utente.getInfoUtilizzatore() if hasattr(utente, 'getInfoUtilizzatore') else {}
        self._email = dati.get('email', '')
        
        self.setWindowTitle("Catalogo Tratte")
        self.resize(400, 400)
        layout = QVBoxLayout()
        
        self.lista_tratte = QListWidget()
        btn_aggiorna = QPushButton("🔄 Aggiorna Catalogo")
        btn_aggiorna.clicked.connect(self.carica_tratte)
        
        btn_bigl = QPushButton("Compra Biglietto Singolo")
        btn_bigl.clicked.connect(lambda: self.compra("Biglietto"))
        btn_carnet = QPushButton("Compra Carnet (10 Viaggi)")
        btn_carnet.clicked.connect(lambda: self.compra("Carnet"))
        
        # preparo il menu a tendina per far scegliere quanto dura l'abbonamento
        self.combo_durata = QComboBox()
        self.combo_durata.addItems(["Settimanale (7 giorni) - 15€", "Mensile (30 giorni) - 50€", "Annuale (365 giorni) - 400€"])
        
        self.campo_data = QDateEdit()
        self.campo_data.setCalendarPopup(True)
        self.campo_data.setDate(QDate.currentDate())
        
        btn_abb = QPushButton("Sottoscrivi Abbonamento")
        btn_abb.clicked.connect(lambda: self.compra("Abbonamento"))
        
        # assemblo tutti i pezzi che ho creato mettendoli in colonna
        layout.addWidget(QLabel("Seleziona una tratta:"))
        layout.addWidget(self.lista_tratte)
        layout.addWidget(btn_aggiorna)
        layout.addWidget(btn_bigl)
        layout.addWidget(btn_carnet)
        layout.addWidget(QLabel("<b>Opzioni Abbonamento:</b>"))
        layout.addWidget(QLabel("Durata:"))
        layout.addWidget(self.combo_durata)
        layout.addWidget(QLabel("Data inizio:"))
        layout.addWidget(self.campo_data)
        layout.addWidget(btn_abb)
        self.setLayout(layout)
        
        # dato che il programma potrebbe bloccarsi dato che sta ancora preparando l'interfaccia gli do un attimo prima di fargli caricare la lista
        QTimer.singleShot(1, self.carica_tratte)

    def carica_tratte(self):
        # pulisco la lista e chiedo al gestore di darmi tutte le tratte disponibili
        self.lista_tratte.clear()
        try:
            tratte = self._gestore_tratte.ricerca_tratta()
            if not tratte:
                self.lista_tratte.addItem("Nessuna tratta.")
                return
            self.lista_tratte.addItems([str(t) for t in tratte])
        except Exception as e:
            self.lista_tratte.addItem(f"Errore: {e}")

    def compra(self, tipo):
        # guardo quale tratta ha selezionato dall'elenco
        item = self.lista_tratte.currentItem()
        if not item or "Nessuna" in item.text() or "Errore" in item.text():
            QMessageBox.warning(self, "Attenzione", "Seleziona una tratta valida!")
            return
            
        data = None
        durata = None
        
        if tipo == "Abbonamento":
            # tiro fuori i suoi dati e guardo quanti giorni ha selezionato dal menu
            data = self.campo_data.date().toString("dd/MM/yyyy")
            scelta = self.combo_durata.currentText()
            
            if "7" in scelta:
                durata = 7
            elif "30" in scelta:
                durata = 30
            else:
                durata = 365

        # passo tutti i dati raccolti al gestore per creare il biglietto
        esito = self._gestore_titoli.creaTitoloViaggio(item.text(), self._email, tipo, data, durata)
        
        if esito:
            QMessageBox.information(self, "Successo", f"{tipo} acquistato!")
        else:
            QMessageBox.warning(self, "Errore", "Acquisto fallito.")


# area di test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    print("avvio il test per la schermata degli acquisti")
    
    # mi creo dei finti gestori e un finto utente solo per far aprire la finestra grafica senza errori
    class FintoGestoreTratte:
        def ricerca_tratta(self):
            return ["roma - milano (08:00) a 50.0€", "napoli - firenze (10:00) a 30.0€"]
            
    class FintoGestoreTitoli:
        def creaTitoloViaggio(self, tratta, email, tipo, data, durata):
            print("finto acquisto di un", tipo, "sulla tratta", tratta)
            return True
            
    class FintoUtente:
        def getInfoUtilizzatore(self):
            return {"email": "test@mail.it"}
            
    app = QApplication(sys.argv)
    finestra_prova = VistaAcquisti(FintoGestoreTratte(), FintoGestoreTitoli(), FintoUtente())
    finestra_prova.show()
    sys.exit(app.exec())