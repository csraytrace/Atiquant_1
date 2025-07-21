from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re


Elemente = [(0,"O"),(8775, 'Al'), (23689, 'Si'), (1632, 'S'), (7517, 'K'), (7415, 'Ca'), (11861, 'Ti'), (357772, 'Fe'), (2365, 'Zn'), (2930, 'As'), (2718, 'Rb'), (20272, 'Sr'), (2801, 'Y'), (9421, 'Zr')]
Übergänge =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Z_gemittelt=12

#Elemente = [(0,"C"),(8775, 'Al'), (23689, 'Si'), (1632, 'S'), (7517, 'K'), (7415, 'Ca'), (11861, 'Ti'), (357772, 'Fe'), (2365, 'Zn'), (2930, 'As'), (2718, 'Rb'), (20272, 'Sr'), (2801, 'Y'), (9421, 'Zr')]
#Z_gemittelt=11
Verteilung=[1]

Elemente = [(0,"H"), (0,"C"), (0,"N"),(0,"O"),(8775, 'Al'), (23689, 'Si'), (1632, 'S'), (7517, 'K'), (7415, 'Ca'), (11861, 'Ti'), (357772, 'Fe'), (2365, 'Zn'), (2930, 'As'), (2718, 'Rb'), (20272, 'Sr'), (2801, 'Y'), (9421, 'Zr')]
Übergänge =  [0,0,0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Verteilung=[5,10,1,10]
Z_gemittelt=11.3

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=600, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)

#print(P1)
#op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True)



op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,latex=True,binder=[[3,0.9],["1 C38H76N2O2"]])
Start = np.append(op_Konz, op_Geo)
Start = op_Konz
Start=Start.tolist()

op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,10))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,15))
