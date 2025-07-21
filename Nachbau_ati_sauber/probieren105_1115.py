from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re


Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(5133, 'P'), (10712, 'S'), (106811, 'K'), (149371, 'Ca'), (2612, 'Mn'), (5666, 'Fe'), (17511, 'Sr')]
Übergänge = [0,0,0,0,0, 0, 0, 0, 0, 0, 0]



Z_gemittelt=6


Verteilung = [1.29871134, 11.33091673,  1.1731461,   1.37485863]
#Verteilung = [0, 11.33091673,  0,   0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)


#Ki.Apple_test()

op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung)
print(Konzentration)
print(P1)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print(op_Konz)
print(op_Konz.sum())
