from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re



Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(255053, 'P'), (1023646, 'Ca'), (2643, 'Fe'), (6467, 'Zn'), (27248, 'Sr')]
Übergänge = [0,0,0,0,0,0, 0, 0, 0]


Z_gemittelt=11.48

#berechnet&2.4515 & 3.1927 & 39.0288 & 15.7755 & 12.9649 & 26.5013 & 0.0207 & 0.0227 & 0.0419 & 8.13e-10 & 11.48 & 1.04e-05 \\
Ver=" 0 H1 + 1 C1 + 0 N1 + 0 O1"
Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])
print(Verteilung)
Verteilung=[2.4515,3.1927,39.0288,15.7755]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)
#Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3*2.5,charzucont=9.46173852e-01/2.5)
#Z_gemittelt+=0.4
#Ki.Knochen_test()

print(P1)
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung)
#print(Konzentration)
#print(P1)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)
#print(op_Konz.sum())



