import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QTabWidget, QFormLayout

class VistaUtenza(QWidget):
    def __init__(self, gestore):
        super().__init__()
        # mi salvo il gestore e preparo la finestra principale mettendo le due schede per il login e la registrazione
        self._gestore = gestore
        self.setWindowTitle("Sistema Trasporti - Accesso")
        self.resize(350, 300)
        
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        
        self.tab_login = QWidget()
        self.tab_registrazione = QWidget()
        self.tabs.addTab(self.tab_login, "Login")
        self.tabs.addTab(self.tab_registrazione, "Registrati")
        
        self._build_login()
        self._build_registrazione()
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def _build_login(self):
        # preparo la schermata per accedere e faccio in modo che la password si oscuri mentre viene digitata
        layout = QVBoxLayout()
        self.log_email = QLineEdit()
        self.log_email.setPlaceholderText("Email")
        self.log_pwd = QLineEdit()
        self.log_pwd.setPlaceholderText("Password")
        self.log_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn_login = QPushButton("Accedi")
        btn_login.clicked.connect(self.on_login)
        
        layout.addWidget(self.log_email)
        layout.addWidget(self.log_pwd)
        layout.addWidget(btn_login)
        self.tab_login.setLayout(layout)

    def _build_registrazione(self):
        # creo il modulo per far iscrivere i nuovi clienti mettendo le etichette di fianco a ogni casella
        layout = QFormLayout()
        self.reg_nome = QLineEdit()
        self.reg_cognome = QLineEdit()
        self.reg_cf = QLineEdit()
        self.reg_email = QLineEdit()
        self.reg_pwd = QLineEdit()
        self.reg_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn_registra = QPushButton("Registra Account")
        btn_registra.clicked.connect(self.on_registrazione)
        
        layout.addRow("Nome:", self.reg_nome)
        layout.addRow("Cognome:", self.reg_cognome)
        layout.addRow("Codice Fiscale:", self.reg_cf)
        layout.addRow("Email:", self.reg_email)
        layout.addRow("Password:", self.reg_pwd)
        layout.addRow(btn_registra)
        self.tab_registrazione.setLayout(layout)

    def on_login(self):
        # prendo l'email e la password scritte tolgo gli spazi vuoti agli estremi e chiedo al gestore se esistono nel sistema
        email = self.log_email.text().strip()
        pwd = self.log_pwd.text().strip()
        
        if not email or not pwd:
            QMessageBox.warning(self, "Attenzione", "Inserisci email e password")
            return
            
        utente = self._gestore.effettua_login(email, pwd)
        if utente:
            if hasattr(self, 'on_login_completato'):
                self.on_login_completato(utente)
        else:
            QMessageBox.warning(self, "Errore", "Credenziali errate.")

    def on_registrazione(self):
        # raccolgo tutti i dati dalle caselle e controllo di non avere campi vuoti prima di passarli al gestore per la registrazione
        n, c, cf, e, p = self.reg_nome.text(), self.reg_cognome.text(), self.reg_cf.text(), self.reg_email.text(), self.reg_pwd.text()
        
        if not all([n, c, cf, e, p]):
            QMessageBox.warning(self, "Attenzione", "Compila tutti i campi")
            return
            
        if self._gestore.registra_cliente(n, c, cf, e, p):
            QMessageBox.information(self, "Successo", "Registrazione ok! Fai il login.")
            # riporto l'utente sulla prima scheda così può fare subito l'accesso
            self.tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Errore", "Email già in uso o password < 8 caratteri.")


# area di test
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    print("avvio il test per la schermata di utenza e login")
    
    # preparo un finto gestore che finge di approvare login e registrazioni
    class FintoGestoreUtenza:
        def effettua_login(self, email, password):
            print("simulo il login con email:", email)
            # restituisco un finto utente giusto per far passare il controllo
            return True
            
        def registra_cliente(self, nome, cognome, cf, email, password):
            print("simulo la registrazione di:", nome, cognome)
            return True
            
    app = QApplication(sys.argv)
    finestra_prova = VistaUtenza(FintoGestoreUtenza())
    
    # aggiungo una finta funzione di completamento per non far arrabbiare il programma quando il login ha successo
    def finto_smistamento(utente):
        print("login andato a buon fine passo alla schermata successiva")
        
    finestra_prova.on_login_completato = finto_smistamento
    
    finestra_prova.show()
    sys.exit(app.exec())