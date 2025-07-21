from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Verbindung = "0.02 Ni1 O1 + 0.465 Sn1 O2 + 0.355 Ti1 O2 + 0.16 Zr1 O2"
print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))


Elemente = [(0,"O"),(7982, "P"),(62131, "Ti"), (26804, "Ni"), (571570, "Zr"), (193410, "Sn")]
Übergänge = [0, 0, 0, 0, 0,0]

Elemente = [(0,"O"),(62131, "Ti"), (26804, "Ni"), (571570, "Zr"), (193410, "Sn")]
Übergänge = [0, 0, 0, 0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#P1=[8, 38, 40, 41, 30, 56, 1]

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())
Startwerte = [0,0.02106275, 0.25260578, 0.02551868, 0.1826614, 0.5181514, 7.44582595e-06]



print(P1)
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(30.46)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

print(P1)
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(30.46)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


Elemente = [(0,"O"),(62131, "Ti"), (26804, "Ni"), (571570, "Zr"), (193410, "Sn")]
Übergänge = [0, 0, 0, 0,0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])


Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())
Startwerte = [0, 0.25260578, 0.02551868, 0.1826614, 0.5181514, 7.44582595e-06]

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(30.46,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(30.46)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
Ki.Minimierung_dark(30.46,[1])
