from Przedmiot import Przedmiot

class Bilet(Przedmiot):
    def __init__(self, nazwa, cena, id, obrazek, typ):
        Przedmiot.__init__(self, nazwa, cena, id, obrazek) #uruchamiam konstruktor Przedmiotu
        self._typ = typ
        #self._ile_w_koszyku = 0

