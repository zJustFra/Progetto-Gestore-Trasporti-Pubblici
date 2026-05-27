import sys
from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox

class VistaAmministratore(QWidget):
    def __init__(self, gestore_tratte):
        super().__init__()
        # mi aggancio al gestore delle tratte e metto il titolo alla finestra
        self._gestore = gestore_tratte
        self.setWindowTitle("Amministrazione - Aggiungi Tratta")
        
        # preparo le caselle di testo vuote e il bottone per confermare
        layout = QFormLayout()
        self.p = QLineEdit()
        self.a = QLineEdit()
        self.o = QLineEdit()
        self.pr = QLineEdit()
        
        btn = QPushButton("Salva Tratta")
        btn.clicked.connect(self.salva)
        
        # assemblo l'interfaccia mettendo le etichette giuste di fianco a ogni casella
        layout.addRow("Partenza:", self.p)
        layout.addRow("Arrivo:", self.a)
        layout.addRow("Orari:", self.o)
        layout.addRow("Prezzo:", self.pr)
        layout.addRow(btn)
        self.setLayout(layout)

    def salva(self):
        try:
            # trasformo la virgola in punto nel caso venga usata per i decimali, cosìevita di bloccarsi
            prezzo = float(self.pr.text().replace(',', '.'))
            
            # passo i testi estratti dalle caselle al gestore per creare la nuova tratta
            esito = self._gestore.aggiungi_tratta(self.p.text(), self.a.text(), self.o.text(), prezzo)
            
            # se il gestore mi risponde con un testo vuol dire che mi sta mandando un messaggio di errore
            if isinstance(esito, str): 
                QMessageBox.warning(self, "Errore", esito)
            else:
                QMessageBox.information(self, "Ok", "Tratta inserita!")
                # svuoto tutte le caselle di testo per renderle pronte a un nuovo inserimento
                self.p.clear(); self.a.clear(); self.o.clear(); self.pr.clear()
        except Exception:
            # se nel campo del prezzo mi scrivono delle lettere invece dei numeri blocco tutto e avviso
            QMessageBox.warning(self, "Errore", "Prezzo non valido.")


# area di test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    print("avvio il test per la schermata dell'amministratore")
    
    # creo un finto gestore al volo per far funzionare l'interfaccia senza toccare i file veri
    class FintoGestoreTratte:
        def aggiungi_tratta(self, partenza, arrivo, orari, prezzo):
            print("finto inserimento tratta da", partenza, "a", arrivo, "al prezzo di", prezzo)
            return True
            
    app = QApplication(sys.argv)
    finestra_prova = VistaAmministratore(FintoGestoreTratte())
    finestra_prova.show()
    sys.exit(app.exec())