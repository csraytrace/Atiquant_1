from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re


Verbindung="71.13 Si1O2 + 12.74 Na2O1 + 10.71 Ca1O1 + 2.76 Al2O3 + 2.01 K2O1 + 0.27 Mg1O1 + 0.13 S1O3 +0.12 Ba1O1 +0.04 Fe2O3 + 0.03 As2O3 + 0.014 Ti1O2 + 0.007 Zr1O2"
x,y,z=(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))
print(x,y,z)
y=np.array(y)
y*=100
print(" & ".join([f"{value:.2f}" for value in y]))
