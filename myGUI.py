from appJar import gui
import Pieniadze as p
import Automat as a
from Bilet import Bilet

automat = a.Automat()

pieniadzeWrzucone = p.Pieniadze() # chyba wywalic

przedmiot = [None for _ in range(6)] #[None] * 6
przedmiot[0] = Bilet("bilet ulgowy (20 min)", 200, "20u", "img/20u.gif", "U")
przedmiot[1] = Bilet("bilet normalny (20 min)", 280, "20n", "img/20n.gif", "N")
przedmiot[2] = Bilet("bilet ulgowy (40 min)", 190, "40u", "img/40u.gif", "U")
przedmiot[3] = Bilet("bilet normalny (40 min)", 380, "40n", "img/40n.gif", "N")
przedmiot[4] = Bilet("bilet ulgowy (60 min)", 290, "60u", "img/60u.gif", "U")
przedmiot[5] = Bilet("bilet normalny (60 min)", 500, "60n", "img/60n.gif", "N")



def aktualizacja():

    zlotowki = lambda x: (x / 100)

    w_automacie = "Do automatu wrzucono " + str(zlotowki(automat.pokaz_stan(2))) + " zł"
    app.setLabel("wrzucone", w_automacie)

    stan = "Pieniędzy w automacie " + str(zlotowki(automat.pokaz_stan(1))) + " zł (" + str(
        zlotowki(automat.pokaz_stan(3))) + " zł)"
    app.setLabel("aktualnystan", stan)

    u = automat.zwroc_slownik(3)
    g = list(u.keys())
    h = list(u.values())

    for i in range(14):
        app.setPieChart("wykres", g[i], h[i]) # sprawdzić dla 0

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def launch(win):
    app.showSubWindow(win)

app=gui("Implementacja Automatu Biletowego MPK")
app.setSticky("news")
app.setExpand("both")


def podajIlosc(przedmiot):
    tekst = "Proszę podać ilość biletów\n" + przedmiot.zwrocNazwe() + "\n"
    ilosc = app.textBox("Podaj ilość", tekst)

    if ilosc is None:
        ilosc = 0

    if ((RepresentsInt(ilosc)) and (int(ilosc) >= 0)):
        for i in range(int(ilosc)):
            app.addListItem("koszyk", przedmiot.zwrocNazwe())
    else:
        app.warningBox("Błąd", "Proszę podać wartość całkowitą, większą lub równą zero!")


# glowne okno
def press(btn):

    for i in range(6):
        if btn == przedmiot[i].zwrocID():
            podajIlosc(przedmiot[i])

    if btn == "Pokaż dokładny stan automatu":
        tekst = automat.zwroc_stan(1)
        app.infoBox("Stan Automatu", tekst)
    if btn == "Pokaż dokładne wrzucone":
        tekst = automat.zwroc_stan(2)
        app.infoBox("Pieniądze aktualnie wrzucone", tekst)

    if btn == "Usuwanie":
        items = app.getListItems("koszyk")
        if len(items) > 0:
            app.removeListItem("koszyk", items[0])
    if btn == "Czyszczenie":
        app.clearListBox("koszyk")

    if btn == "Wpłać pieniądze":
        x = automat.zwroc_wartosci(1)
        y = [0 for _ in range(14)] #[0] * 14

        y[0] = app.getEntry("0.01zł")
        y[1] = app.getEntry("0.02zł")
        y[2] = app.getEntry("0.05zł")
        y[3] = app.getEntry("0.10zł")
        y[4] = app.getEntry("0.20zł")
        y[5] = app.getEntry("0.50zł")
        y[6] = app.getEntry("1.00zł")
        y[7] = app.getEntry("2.00zł")
        y[8] = app.getEntry("5.00zł")
        y[9] = app.getEntry("10.00zł")
        y[10] = app.getEntry("20.00zł")
        y[11] = app.getEntry("50.00zł")
        y[12] = app.getEntry("100.00zł")
        y[13] = app.getEntry("200.00zł")

        licznik = 0

        for i in y:
            if (float(i).is_integer() and (int(i) >= 0)):
                licznik += 1
                i = int(i)
            else:
                i = int(0)
                app.warningBox("Błąd", "Proszę podać wartośći całkowite, większe lub równe zeru!")
                break

        if(licznik == 14):
            h = automat.zwroc_slownik(2)
            stara = list(h.values())
            nowa = y

            y = [a + b for a, b in zip(stara, nowa)]
            automat.wplataP(y)
            automat.zmiana()

            aktualizacja()

    if btn == "Zwrot pieniędzy":
        automat.zwrot()
        aktualizacja()

    if btn == "Zapłać":
        zakupy = app.getListItems("koszyk")

        if not zakupy:
            app.warningBox("Błąd", "Za co chcesz zapłacić? jak nic nie wybrałeś!")
        else:
            if automat.pokaz_stan(2) != 0:
                tekst = "Czy napewno chcesz zakupić: \n\n"

                licznik = [0] * 6
                do_zaplaty = [0] * 6
                suma = 0

                for k in range(6):
                    for a in zakupy:
                        if a == przedmiot[k].zwrocNazwe():
                            licznik[k] += 1
                            do_zaplaty[k] += przedmiot[k].zwrocCene()

                for k in range(6):
                    suma += do_zaplaty[k]
                    tekst += przedmiot[k].zwrocNazwe()
                    tekst += "\t "
                    tekst += str(licznik[k])
                    tekst += " x "
                    tekst += str(przedmiot[k].zwrocCene() / 100)
                    tekst += "\t= "
                    tekst += str(do_zaplaty[k] / 100)
                    tekst += " zł"
                    tekst += "\n"
                tekst += "-" * 50
                tekst += "\nrazem do zapłaty:\t "
                tekst += str(suma / 100)
                tekst += " zł"

                if (app.yesNoBox("Zakup", tekst)) == True:
                    wynik = automat.oblicz_reszte(suma)

                    if wynik == "nie ma jak wydac":
                        tekst = "Niestety automat nie ma jak wydać!\nAutomat zwraca to co dostał\n\n" + str(
                            automat.zwroc_stan(2))
                        app.warningBox("Błąd", tekst)

                        automat.wplataP([0] * 14)
                        aktualizacja()
                    elif wynik == "zakup bez reszty":
                        app.infoBox("Potwierdzenie", "Dziękujemy za zakup biletów za odliczoną kwotę!\n")
                        aktualizacja()
                    elif wynik == "za mała wpłata":
                        app.warningBox("Błąd", "Niestety ale musisz jeszcze dopłacić!")
                    else:
                        tekst = "Dziękujemy za zakup biletów\n Twoja reszta:\n"

                        for x in wynik.items():
                            tekst += str(int(x[0]) / 100)
                            tekst += " zł\tx "
                            tekst += str(int(x[1]))
                            tekst += "\n"

                        app.infoBox("Potwierdzenie", tekst)
                        aktualizacja()



                else:
                    pass
            else:
                app.warningBox("Błąd", "A pieniądze kto wrzuci??!")




app.setFont(10)
app.addLabel("l1", "Implementacja Automatu Biletowego Komunikacji Miejskiej", 0, 0, 4, 0)
app.setLabelBg("l1", "yellow")


app.startLabelFrame("Dodaj bilety") # poczatek grupy bilety

app.addButton(przedmiot[0].zwrocID(), press, 1, 0, 0, 0)
app.setButtonImage(przedmiot[0].zwrocID(), przedmiot[0].zwrocObrazek())
app.addButton(przedmiot[1].zwrocID(), press, 1, 1, 0, 0)
app.setButtonImage(przedmiot[1].zwrocID(), przedmiot[1].zwrocObrazek())

app.addButton(przedmiot[2].zwrocID(), press, 2, 0, 0, 0)
app.setButtonImage(przedmiot[2].zwrocID(), przedmiot[2].zwrocObrazek())
app.addButton(przedmiot[3].zwrocID(), press, 2, 1, 0, 0)
app.setButtonImage(przedmiot[3].zwrocID(), przedmiot[3].zwrocObrazek())

app.addButton(przedmiot[4].zwrocID(), press, 3, 0, 0, 0)
app.setButtonImage(przedmiot[4].zwrocID(), przedmiot[4].zwrocObrazek())
app.addButton(przedmiot[5].zwrocID(), press, 3, 1, 0, 0)
app.setButtonImage(przedmiot[5].zwrocID(), przedmiot[5].zwrocObrazek())

app.stopLabelFrame() # koniec grupy bilety


##############################
app.startLabelFrame("Stan różnych nominałów w automacie", 1, 1, 0, 1)
app.addPieChart("wykres", automat.zwroc_slownik(3))

stan = "Pieniędzy w automacie " + str(automat.pokaz_stan(1) / 100) + " zł (" + str(automat.pokaz_stan(3) / 100) + " zł)"
app.addLabel("aktualnystan", stan)

w_automacie = "Do automatu wrzucono " + str(pieniadzeWrzucone.oblicz_wartosc()/100) + " zł" #zaktualizować ale i tak jest 0
app.addLabel("wrzucone", w_automacie)


app.addButtons(["Pokaż dokładny stan automatu","Pokaż dokładne wrzucone"], press)

app.stopLabelFrame()
##############################

##############################
app.startLabelFrame("Wybierz bilety", 2, 0, 1, 0)
app.addListBox("koszyk",[], 0,0,0,5)
app.setListBoxMulti("koszyk", multi=True)


app.addButton("Usuwanie",press,0,1,0,0)
app.addButton("Czyszczenie",press,1,1,0,0)
app.addButton("Zwrot pieniędzy",press,2,1,0,0)
app.addButton("Wpłać pieniądze",press,3,1,0,0)
app.addButton("Zapłać",press,4,1,0,0)



app.stopLabelFrame()
##############################
app.startLabelFrame("Pieniądze do wrzucenia", 2, 1, 2, 0)


app.addLabel("label1", "0.01 zł",0,0,0,0)
app.addNumericEntry("0.01zł",0,1,0,0)
app.setEntryDefault("0.01zł", "ile 1 groszówek")

app.addLabel("label2", "0.02 zł",1,0,0,0)
app.addNumericEntry("0.02zł",1,1,0,0)
app.setEntryDefault("0.02zł", "ile 2 groszówek")

app.addLabel("label3", "0.05 zł",2,0,0,0)
app.addNumericEntry("0.05zł",2,1,0,0)
app.setEntryDefault("0.05zł", "ile 5 groszówek")

app.addLabel("label4", "0.10 zł",3,0,0,0)
app.addNumericEntry("0.10zł",3,1,0,0)
app.setEntryDefault("0.10zł", "ile 10 groszówek")

app.addLabel("label5", "0.20 zł",4,0,0,0)
app.addNumericEntry("0.20zł",4,1,0,0)
app.setEntryDefault("0.20zł", "ile 20 groszówek")

app.addLabel("label6", "0.50 zł",5,0,0,0)
app.addNumericEntry("0.50zł",5,1,0,0)
app.setEntryDefault("0.50zł", "ile 50 groszówek")

app.addLabel("label7", "1.00 zł",6,0,0,0)
app.addNumericEntry("1.00zł",6,1,0,0)
app.setEntryDefault("1.00zł", "ile złotówek")

app.addLabel("label8", "2.00 zł",0,3,0,0)
app.addNumericEntry("2.00zł",0,4,0,0)
app.setEntryDefault("2.00zł", "ile 2-złotówek")

app.addLabel("label9", "5.00 zł",1,3,0,0)
app.addNumericEntry("5.00zł",1,4,0,0)
app.setEntryDefault("5.00zł", "ile 5-złotówek")

app.addLabel("label10", "10.00 zł",2,3,0,0)
app.addNumericEntry("10.00zł",2,4,0,0)
app.setEntryDefault("10.00zł", "ile dziesiątek")

app.addLabel("label11", "20.00 zł",3,3,0,0)
app.addNumericEntry("20.00zł",3,4,0,0)
app.setEntryDefault("20.00zł", "ile dwudziestek")

app.addLabel("label12", "50.00 zł",4,3,0,0)
app.addNumericEntry("50.00zł",4,4,0,0)
app.setEntryDefault("50.00zł", "ile pięćdziesiątek")

app.addLabel("label13", "100.00 zł",5,3,0,0)
app.addNumericEntry("100.00zł",5,4,0,0)
app.setEntryDefault("100.00zł", "ile setek")

app.addLabel("label14", "200.00 zł",6,3,0,0)
app.addNumericEntry("200.00zł",6,4,0,0)
app.setEntryDefault("200.00zł", "ile dwusetek")

app.stopLabelFrame()


app.go()