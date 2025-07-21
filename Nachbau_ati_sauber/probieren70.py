from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

print(zahl_zu_string(9121))

def counter(Übergänge, array):
    sum = 0
    for über in array:
        if über[0] in Übergänge:
            sum += über[1]
    return sum

Kbeta = [" K-M1", " K-M2", " K-M3", " K-M4", " K-M5"]
Kalpha = [" K-L1", " K-L2", " K-L3"]
Lalpha = ["L3-M4", "L3-M5"]

ce = Element(Element="ce")
print(ce.Kanten())
print(ce.Ubergange())
#Verbindung="Ce1S1O8H8"
#print(Verbindung_einlesen(Verbindung)[0])
#print(Verbindung_einlesen(Verbindung)[1])
Verbindung="Ce1S2O12H8"
print(Verbindung_einlesen(Verbindung)[0])
print(Verbindung_einlesen(Verbindung)[1])
#Übergänge=[1,0,0,0]
Übergänge=[0,0,0,0]
for i in range(7):
    #Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01, Einfallswinkelalpha=25,Einfallswinkelbeta=65,P1=Verbindung_einlesen(Verbindung)[0], Konzentration=Verbindung_einlesen(Verbindung)[1], Emax=40+i, Übergänge=Übergänge)
    Ki = Calc_I(Messzeit=100, Röhrenstrom=0.01,P1=Verbindung_einlesen(Verbindung)[0], Konzentration=Verbindung_einlesen(Verbindung)[1], Emax=40+i, Übergänge=Übergänge)

    counts, add = Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])
    Geo = 5.5*10**-6
    print("Emax:", 40+i,counts*Geo)
    print("Kbeta ce",counter(Kbeta,add_format(add, Geo)[0]))
    #print("Kalpha ce",counter(Kalpha,add_format(add, Geo)[0]))
    print("Lalpha ce",counter(Lalpha,add_format(add, Geo)[0]))


    #print("Emax:", 40+i,Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[0]*5.5*10**-6)
    #print("Emax:", 40+i,Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[1])
    #print(add_format(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[1],4*10**-6))
    #print(add_format(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[1],4*10**-6)[0])
    #print("Kbeta ce",counter(Kbeta,add_format(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[1],5.5*10**-6)[0]))

