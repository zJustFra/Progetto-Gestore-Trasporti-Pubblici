class Utilizzatore:
    # classe base per tutti, mi salvo i dati in comune per non doverli riscrivere ogni volta
    def __init__(self, email: str, password: str, nome: str, cognome: str):
        self._email = email
        self._password = password
        self._nome = nome
        self._cognome = cognome

    def getInfoUtilizzatore(self) -> dict:
        # metto tutto in un dizionario, così faccio prima a salvarli in blocco dopo
        return {
            "email": self._email,
            "password": self._password,
            "nome": self._nome,
            "cognome": self._cognome
        }

class Cliente(Utilizzatore):
    def __init__(self, email: str, password: str, nome: str, cognome: str, codice_fiscale: str):
        # passo i dati base su alla classe padre e mi tengo solo il cf da gestire qui
        super().__init__(email, password, nome, cognome)
        self._codiceFiscale = codice_fiscale

    def getInfoUtilizzatore(self) -> dict:
        # prendo il dizionario di base e ci aggiungo i dati specifici del cliente
        info = super().getInfoUtilizzatore()
        info.update({"codiceFiscale": self._codiceFiscale, "ruolo": "Cliente"})
        return info

class Amministratore(Utilizzatore):
    def __init__(self, email: str, password: str, nome: str, cognome: str, livello_accesso: int = 1):
        # stessa cosa, mando i dati in alto e mi salvo solo il livello di accesso
        super().__init__(email, password, nome, cognome)
        self._livelloAccesso = livello_accesso

    def getInfoUtilizzatore(self) -> dict:
        # prendo le info base e ci butto dentro livello e ruolo
        info = super().getInfoUtilizzatore()
        info.update({"livelloAccesso": self._livelloAccesso, "ruolo": "Amministratore"})
        return info

class Controllore(Utilizzatore):
    def __init__(self, email: str, password: str, nome: str, cognome: str, matricola: str):
        # qui invece mi serve solo salvare la matricola
        super().__init__(email, password, nome, cognome)
        self._matricola = matricola

    def getInfoUtilizzatore(self) -> dict:
        # appiccico la matricola e il ruolo al pacchetto di base
        info = super().getInfoUtilizzatore()
        info.update({"matricola": self._matricola, "ruolo": "Controllore"})
        return info


# zona di test: parte solo se avvio direttamente questo file
if __name__ == "__main__":
    print("test per vedere se i modelli girano bene")
    
    # creo un cliente finto per prova
    cliente_prova = Cliente("mario@mail.it", "pass123", "mario", "rossi", "mrrss80...")
    print("dati cliente:", cliente_prova.getInfoUtilizzatore())
    
    # provo con un controllore
    ctrl_prova = Controllore("luigi@mail.it", "ctrl123", "luigi", "verdi", "mat123")
    print("dati controllore:", ctrl_prova.getInfoUtilizzatore())
    
    print("tutto a posto, test finito.")