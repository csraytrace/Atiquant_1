from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re



Elemente = [(0,"O"),  (40870, 'Si'), (4999, 'K'), (37671, 'Ca'), (310, 'Ti'), (1214, 'Fe'), (4441, 'As'), (1300, 'Rb'), (3390, 'Sr'), (3214, 'Zr')]
Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Z_gemittelt=11.4

Verteilung=[1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)

print(P1)
#op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True)
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung)


"""
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,binder=[[2,1],["1 O2"]])    #,low_verteilung_volumenprozent=True,

Start = np.append(op_Konz, op_Geo)
Start = op_Konz
Start=Start.tolist()

op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,5))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,10))
"""
#print(Konzentration)
#print(P1)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)
#print(op_Konz.sum())



