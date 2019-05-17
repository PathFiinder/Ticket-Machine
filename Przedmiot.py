class Przedmiot:
    def __init__(self, nazwa, cena, id, obrazek):
        self._nazwa = nazwa
        self._cena = cena
        self._id = id
        self._obrazek = obrazek
        self._ile_w_koszyku = 0

    def zwrocCene(self):
        return self._cena

    def zwrocNazwe(self):
        return self._nazwa

    def zwrocObrazek(self):
        return self._obrazek

    def zwrocID(self):
        return self._id

    def zwrocIleWKoszyku(self):
        return self._ile_w_koszyku