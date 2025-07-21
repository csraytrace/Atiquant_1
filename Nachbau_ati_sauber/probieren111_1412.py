from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re





Elemente = [(0,"O"),(22777, 'Si'), (3886, 'S'), (9545, 'K'), (12223, 'Ca'), (10328, 'Ti'), (231004, 'Zn'), (447506, 'Sr'), (133476, 'Cd'), (170471, 'Pb')]
Übergänge =  [0,0, 0, 0, 0, 0, 0, 0, 0, 1]


Elemente = [(0,"O"), (2313, 'Al'), (22272, 'Si'), (3698, 'S'), (9555, 'K'), (11663, 'Ca'), (225121, 'Zn'), (436840, 'Sr'), (134218, 'Cd'), (10733, 'Ba'), (143131, 'Pb')]
Übergänge =  [0,0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

#Elemente = [(0,"O"), (2313, 'Al'), (22272, 'Si'), (9555, 'K'), (11663, 'Ca'), (225121, 'Zn'), (436840, 'Sr'), (134218, 'Cd'), (10733, 'Ba'), (143131, 'Pb')]
#Übergänge =  [0,0, 0, 0, 0, 0,  0, 0, 1, 1]

Z_gemittelt=21
Z_gemittelt=19

#Ver=" 0 H1 + 1 C1 + 0 N1 + 0 O1"
#Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])

Verteilung=[1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)

print(P1)
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True)
print(op_Konz)
#print(Konzentration)
#print(P1)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)
#print(op_Konz.sum())









