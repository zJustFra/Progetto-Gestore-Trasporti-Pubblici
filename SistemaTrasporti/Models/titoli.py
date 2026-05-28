from datetime import date, timedelta
from abc import ABC, abstractmethod

class TitoloViaggio(ABC):
    # utilizzo ABC per crare una classe astratta che rappresenta solo un concetto astratto per specificare che la classe TitoloViaggio non deve essere creatata direttamente
    # questa mi serve solo come scheletro per i tipi di biglietto veri, non la uso mai da sola
    def __init__(self, codice: str, prezzo: float):
        self._codice = codice
        self._prezzo = prezzo
        self._stato = "Valido"

    def setStato(self, nuovo_stato: str) -> None: self._stato = nuovo_stato
    def get_stato(self) -> str: return self._stato
    def get_codice(self) -> str: return self._codice
    def get_prezzo(self) -> float: return self._prezzo

    @abstractmethod
    def isValido(self) -> bool:
        # lo lascio vuoto perché ogni tipo di biglietto deciderà per i fatti suoi come capire se è ancora buono o no
        pass

class Biglietto(TitoloViaggio):
    def __init__(self, codice: str, prezzo: float):
        super().__init__(codice, prezzo)
        self._obliterato = False

    def timbra(self) -> None: self._obliterato = True
    def isValido(self) -> bool: return not self._obliterato

class Carnet(TitoloViaggio):
    def __init__(self, codice: str, prezzo: float, viaggi_totali: int):
        super().__init__(codice, prezzo)
        self._viaggiResidui = int(viaggi_totali)

    def scalaViaggio(self) -> None:
        # blocco tutto ed evito crash strani se provano a scalare un viaggio quando il carnet è già a zero
        if self._viaggiResidui > 0:
            self._viaggiResidui -= 1
        else:
            raise ValueError("Impossibile scalare: carnet esaurito")

    def get_viaggi_residui(self) -> int: return self._viaggiResidui
    def isValido(self) -> bool: return self._viaggiResidui > 0

class Abbonamento(TitoloViaggio):
    def __init__(self, codice: str, prezzo: float, data_inizio: str, durata_giorni: int):
        super().__init__(codice, prezzo)
        self._dataInizio = data_inizio
        self._durataGiorni = int(durata_giorni)

    def isScaduto(self) -> bool:
        # provo a spezzettare la data per fare il calcolo dei giorni. se il formato è sballato, blocco e lo do per scaduto
        try:
            g, m, a = map(int, self._dataInizio.split('/'))
            inizio = date(a, m, g)
        except ValueError:
            return True
        scadenza = inizio + timedelta(days=self._durataGiorni)
        return date.today() > scadenza

    def isValido(self) -> bool: return not self.isScaduto()

# zona di test
if __name__ == "__main__":
    print("faccio delle prove sui titoli di viaggio")
    
    bigl = Biglietto("B-123", 1.50)
    print("il biglietto appena preso è valido?", bigl.isValido())
    bigl.timbra()
    print("e dopo averlo timbrato?", bigl.isValido())
    
    abb = Abbonamento("A-123", 30.0, "01/01/2020", 30)
    print("un abbonamento del 2020 è valido oggi?", abb.isValido())

    print("\nprovo il carnet")
    carnet = Carnet("C-123", 15.00, 2)
    print("viaggi residui iniziali:", carnet.get_viaggi_residui())
    
    carnet.scalaViaggio()
    print("dopo un viaggio ne rimangono:", carnet.get_viaggi_residui())
    carnet.scalaViaggio()
    print("dopo un altro viaggio è ancora valido?", carnet.isValido())
    
    # provo a far scattare l'errore apposta per vedere se mi blocca
    try:
        carnet.scalaViaggio()
    except ValueError as e:
        print("se provo a viaggiare a scrocco mi blocca e dice:", e)
