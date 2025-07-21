from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Verbindung = "1 Ce1 + 2 S1O4 + 4 H2O1"
print(Verbindungen_Gewichtsprozent(Verbindung))
#print(Gewichtsprozent_Atomprozent(['Ce', 'S', 'O', 'H'], [0.34657677220856437, 0.15861458328180725, 0.4748643421397585, 0.019944302369869858]))

Elemente = [(0,"H"),(0,"O"),(29925, "S"),(79790, "Ce")]
Übergänge = [0,0,0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#P1=[8, 38, 40, 41, 30, 56, 1]

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.01, Messzeit=1000, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())
Startwerte = [0, 0, 0.14259921, 0.85740079, 4.22941158e-06]

print(P1)
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(26.45,Startkonzentration=Startwerte)
#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(32,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print((Ki.Intensität_alle_jit_fürMinimierung([0.019944302369869858,0.4748643421397585,0.15861458328180725,0.34657677220856437])[0]*op_Geo))
