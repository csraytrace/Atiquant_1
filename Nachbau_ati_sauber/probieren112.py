from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re




sr = Element(Element="Sr")
print(sr.Ubergange())



#14.165

Verbindung = '2.4526 H + 3.1941 C + 39.0465 N +  15.7827 O +  12.9581 P + 26.4807  Ca +  0.0207 Fe + 0.0227 Zn +0.0419 Sr'


ele_soil,kon_soil,z_soil = (Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

print(ele_soil,kon_soil, z_soil)


print(Filter(Verbindung, 1, 19))

print(Filter("1 H2O1", 1, 14.165))



Verbindung = '42.38 Si1O2 + 7.52 Al2O3 + 4.53 Ca1O1 + 4.69 Mg1O1 + 4.55 Sr1O1 + 4.69 Na2O1 + 4.14 K2O1 + 4.5 Li2O1 + 4.53 Ba2O3  + 4.67B1O1 + 4.48 Zn1O1 + 4.4 Pb1O1 + 4.38 Cd1O1 + 0.031 Fe2O3'


ele_soil,kon_soil,z_soil = (Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

print(ele_soil,kon_soil, z_soil)
print(np.array(kon_soil)*100)
