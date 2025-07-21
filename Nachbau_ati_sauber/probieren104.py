from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re


Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(14938, 'P'), (29272, 'S'), (150738, 'K'), (103664, 'Ca'), (14794, 'Fe'), (13076, 'Zn'), (11376, 'Br'), (8352, 'Rb'), (23621, 'Sr')]
Übergänge = [0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0]


#Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(470, "Na"),(14938, 'P'), (29272, 'S'), (150738, 'K'), (103664, 'Ca'), (14794, 'Fe'), (13076, 'Zn'), (11376, 'Br'), (8352, 'Rb'), (23621, 'Sr')]
#Übergänge = [0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0,0]



Z_gemittelt=6.59
Z_gemittelt=6.72114052


#Ver="100 H1 + 10 C1 + 10 N1+ 10 O1"

#Ver="10 H1 + 1 C1 + 1 N1 + 10 O1"
#Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])
#print(Verteilung)
Verteilung = [1.29871134, 11.33091673,  1.1731461,   1.37485863]
Verteilung = [1.02449088, 23.52431594,  0.34032626,  2.39590297]
#Verteilung = [0, 11.33091673,  0,   0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)



op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,fix_konz=[0.5707],latex=True)

#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


###############op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung)


#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(Konzentration)
#print(P1)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)
#print(op_Konz.sum())


"""

Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(397, "Na"),(738,"Mg"),(14938, 'P'), (29272, 'S'), (150738, 'K'), (103664, 'Ca'), (14794, 'Fe'), (13076, 'Zn'), (11376, 'Br'), (8352, 'Rb'), (23621, 'Sr')]
Übergänge = [0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0,0,0]


Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

Konz=op_Konz.tolist()
Konz.insert(4,1.83)
Konz.insert(5,0.9)
#Ki.Intensität_alle_jit_fürMinimierung(Konz)
#print((Ki.Intensität_alle_jit_fürMinimierung(Konz)[0]*op_Geo))
"""


Elemente = [(0,"H"), (0,"C"),(0,"N"),(0,"O"),(397, "Na"),(738,"Mg"),(14938, 'P'), (29272, 'S'), (150738, 'K'), (103664, 'Ca'), (14794, 'Fe'), (13076, 'Zn'), (11376, 'Br'), (8352, 'Rb'), (23621, 'Sr')]
Übergänge = [0,0,0,0,0,0, 0, 0, 0, 0, 0, 0, 0,0,0]


#Z_gemittelt=6.8



#Ver="100 H1 + 10 C1 + 10 N1+ 10 O1"

#Ver="10 H1 + 1 C1 + 1 N1 + 10 O1"
#Ver=" 0 H1 + 1 C1 + 0 N1 + 0 O1"
#Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])
#print(Verteilung)


Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)



op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,fix_konz=[1.82,0.9])
