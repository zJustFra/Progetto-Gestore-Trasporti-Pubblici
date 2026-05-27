import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox

class VistaControllore(QWidget):
    def __init__(self, gestore_titoli):
        super().__init__()
        # mi salvo il gestore dei titoli e metto il titolo alla finestra del terminale
        self._gestore = gestore_titoli
        self.setWindowTitle("Terminale Controllore")
        
        layout = QVBoxLayout()
        self.campo = QLineEdit()
        self.campo.setPlaceholderText("Es. BIGL-1234")
        
        # faccio in modo che il controllo parta in automatico anche se viene premuto il tasto invio sulla tastiera
        self.campo.returnPressed.connect(self.verifica)
        
        btn = QPushButton("Verifica Titolo")
        btn.clicked.connect(self.verifica)
        
        # metto la casella di ricerca ed il bottone uno sopra l'altro
        layout.addWidget(self.campo)
        layout.addWidget(btn)
        self.setLayout(layout)

    def verifica(self):
        # prendo il testo scritto e gli tolgo eventuali spazi vuoti messi per sbaglio all'inizio o alla fine
        codice = self.campo.text().strip()
        
        # se non ha scritto niente blocco l'operazione subito
        if not codice: return
        
        # passo il codice al gestore che controlla se il biglietto è buono e nel caso lo timbra direttamente
        esito = self._gestore.verifica_e_utilizza_titolo(codice)
        QMessageBox.information(self, "Esito", esito)
        
        # svuoto la casella di ricerca così sono pronto al volo per controllare il prossimo passeggero
        self.campo.clear()


# area di test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    print("avvio il test per il terminale del controllore")
    
    # preparo il gestore finto per far aprire la schermata grafica in totale autonomia
    class FintoGestoreTitoli:
        def verifica_e_utilizza_titolo(self, codice):
            print("simulo il controllo e la timbratura del biglietto con codice", codice)
            return "Titolo Valido. Obliterazione confermata."
            
    app = QApplication(sys.argv)
    finestra_prova = VistaControllore(FintoGestoreTitoli())
    finestra_prova.show()
    sys.exit(app.exec())