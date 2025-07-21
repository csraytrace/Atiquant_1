from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *


Verbindung1= "1 Al2O3 "
Verbindung2 = "99.6 Al2O3 + 0.005 Ca1O1 + 0.1 Fe2O3 + 0.15 Mg1O1 + 0.14 Si1O2"

Verbindungen=[Verbindung1,Verbindung2]
#Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindungen)

werte=[]
for Verbindung in Verbindungen:
    print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))
    p1,konz,z=Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung)

    Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=p1, Konzentration=konz)
    print(Ki.Intensität_alle_jit_fürMinimierung(konz)[0])
    #print(werte[-1])



#Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=Verbindung_einlesen("Pb")[0], Konzentration=Verbindung_einlesen("Pb")[1],Übergänge=[1])
#x=(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen("Pb")[1])[0][0])

#Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=Verbindung_einlesen("Pb1O1")[0], Konzentration=Verbindung_einlesen("Pb1O1")[1],Übergänge=[1,0])
#y=(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen("Pb1O1")[1])[0][0])
#print("BleiO-L", y/x)
