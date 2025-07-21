import re
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.Calc_I import *
Verbindung = "0.5 Ca1C1O3 + 0.5 H2O1 "

#print(Verbindung.strip(" ").split("+"))
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import Verbindung_einlesen

#print(Verbindung_einlesen("Ca1C1O3"))
#print(Verbindung_einlesen("Ca 1 C 1 O 3"))


#print(Gewichtsprozent_Atomprozent(['O', 'Sr', 'Zr', 'Nb', 'Zn', 'Ba', 'Ta'],[3.05755018, 0.01838225, 0.00732883, 0.00639168, 0.20869838, 1.56094735,
# 1.24792115]))
#print(Verbindungen_Gewichtsprozent("1 O8.97554825e-01 Sr9.85377848e-04 Zr3.77356604e-04 Nb3.23131009e-04 Zn1.49927582e-02 Ba5.33746878e-02 Ta3.23918635e-02"))
    #print(Gesamtgewicht)

    #print(Elemente_anzahl)
    #print(Verbindung_konz)

    #return Elemente, np.array([mas.Get_Atomicweight() * Atomzahl[index_j] / Gesamtgewicht for index_j, mas in enumerate(Element_fkt)])

#print(Atomprozent_Verbindungen(Verbindung))
#Verbindung = "0.5 Ca1C1O3 + 1 H2O1 "
#print(Atomprozent_Verbindungen(Verbindung))
#Verbindung = "0.5 Ca1C1O3 + 0.5 H2O1 + 0.5 H2O1"
#print(Atomprozent_Verbindungen(Verbindung))
#Verbindung = "0.5 Ca1C1O3 + 100 H2O1 + 0.5 H2O1"
#print(Atomprozent_Verbindungen(Verbindung))
#Verbindung = "0.2 Ca1C1O3"
#print(Atomprozent_Verbindungen(Verbindung))
#print(Verbindung_einlesen("Ca1C1O3"))
Verbindung = "0.466 Ba1 O1 + 0.45 Ta2 O3 + 0.084 Zn1 O1"
#print(Verbindungen_Gewichtsprozent(Verbindung))

#print(Verbindungen_Gewichtsprozent(Verbindung))
#print(Verbindungen_Gewichtsprozent(Verbindung, Massenprozent=True))
#print(Verbindung_einlesen("Ta2O3"))
print(Verbindungen_Gewichtsprozent_vonMassenprozent("1 Ba1O1 + 1 Ce1O2"))
# Testen mit Beispielwerten
#verbindungen = "2 Ba1O1 + 1 Ce1O2 + 1 O 3 Ce3"
konz_liste, verbindungen_liste, Z = Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung)

print("Liste der entfernten Zahlen:", konz_liste)  # [1.0, 1.0]
print("Bereinigte Verbindungen:", verbindungen_liste)  # ['Ba1O1', 'Ce1O2']
print("Z",Z)

Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [0, 0 , 1, 1]

#Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
#Übergänge = [0, 0 , 1, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

print(Konzentration)
print(Ki.Intensität_alle_jit_fürMinimierung([0.1178285254533203, 0.06748488572130745, 0.41738236828377673, 0.3973042205415955])[0]*6.485184069217674e-06)


Elemente = [(0, "O"),(6962, "Sr"), (3290, "Zr"), (3123, "Nb"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [0, 0, 0, 0, 0, 1, 1]

#Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
#Übergänge = [0, 0 , 1, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

print(Konzentration)
print(Ki.Intensität_alle_jit_fürMinimierung([10.677110089851194,0.53840455,  0.21465676,  0.18720826,  6.11264335, 45.71915787, 36.55081914])[0]*6.485184069217674e-06)

ati = np.array([0.00640349, 0.00255382, 0.00222813, 0.07043534, 0.49787731,0.42050191])
ati=ati * (1-0.10677110089851194)
ati=np.insert(ati, 0, 0.10677110089851194)
print(ati,ati.sum())
print(Ki.Intensität_alle_jit_fürMinimierung(ati)[0]*6.32805013e-06)



Elemente = [(6962, "Sr"), (3290, "Zr"), (3123, "Nb"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [ 0, 0, 0, 0, 1, 1]

#Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
#Übergänge = [0, 0 , 1, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

print(Ki.Atiquant())
