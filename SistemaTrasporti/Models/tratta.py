class Tratta:
    """Entity che modella una tratta del servizio di trasporto."""
    def __init__(self, id_tratta: int, partenza: str, arrivo: str, orari: str, prezzo: float):
        self._id_tratta = id_tratta
        self._partenza = partenza
        self._arrivo = arrivo
        self._orari = orari
        self._prezzo = prezzo

    def get_id_tratta(self) -> int: return self._id_tratta
    def get_partenza(self) -> str: return self._partenza
    def get_arrivo(self) -> str: return self._arrivo
    def get_orari(self) -> str: return self._orari
    def get_prezzo(self) -> float: return self._prezzo

    def __str__(self) -> str:
        # imposto come voglio che si veda la tratta a schermo nelle liste dell'interfaccia grafica
        return f"[ID: {self._id_tratta}] {self._partenza} - {self._arrivo} ({self._orari}) a {self._prezzo}€"

# zona di test
if __name__ == "__main__":
    print("creo una tratta al volo...")
    tratta_prova = Tratta(1, "roma", "milano", "08:00 - 11:00", 45.50)
    
    # stampo per controllare se il metodo __str__ formatta bene il tutto
    print(tratta_prova)