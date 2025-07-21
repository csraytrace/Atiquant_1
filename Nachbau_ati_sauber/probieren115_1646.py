from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re

Elemente = [(0,"C"),(3750, 'Al'), (30615, 'Si'), (3383, 'S'), (7173, 'K'), (4830, 'Ca'), (5386, 'Ti'), (1697, 'Mn'), (155448, 'Fe'), (1536, 'Zn'), (3058, 'Br'), (2557, 'Rb'), (5464, 'Sr'), (1880, 'Y'), (18974, 'Zr')]
Übergänge =  [0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Z_gemittelt=10.5
Z_gemittelt=9.8
#Z_gemittelt=10


Elemente = [(0,"H"), (0,"C"), (0,"N"),(0,"O"),(3750, 'Al'), (30615, 'Si'), (3383, 'S'), (7173, 'K'), (4830, 'Ca'), (5386, 'Ti'), (1697, 'Mn'), (155448, 'Fe'), (1536, 'Zn'), (3058, 'Br'), (2557, 'Rb'), (5464, 'Sr'), (1880, 'Y'), (18974, 'Zr')]
Übergänge =  [0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Z_gemittelt=10.5
Z_gemittelt=9.8


Verteilung=[5,10,1,10]
#Verteilung=[2.9812 , 17.7602 , 1.0903 , 48.7216]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=600, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)

print(P1)
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True,binder=[[3,0.9],["1 C38H76N2O2"]])
#op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True)

Start = np.append(op_Konz, op_Geo)
Start = op_Konz
Start=Start.tolist()

#op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,5))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,10))




