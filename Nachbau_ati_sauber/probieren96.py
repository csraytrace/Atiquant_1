import numpy as np


from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

[2,1,0,1]
binder=([0.25,0.5,0.25],["1 H1C1O1","1 h1"])
#print(binder[1])
#print(Verbindungen_Gewichtsprozent_vonMassenprozent(binder[1][0]))
#print(Verbindungen_Gewichtsprozent_vonMassenprozent("1C38H76N2O2"))
#Verbingung="H5O1C2"

#print(Verbindung_einlesen(Verbingung))
print(Verbindungen_Gewichtsprozent_vonMassenprozent("0.5 H1 + 0.25 C1 + 0.0 N1 + 0.25 O1"))
print(Verbindungen_Gewichtsprozent("0.5 H1 + 0.25 C1 + 0.0 N1 + 0.25 O1"))
print(Verbindungen_Gewichtsprozent_vonMassenprozent("0.5 H2C1O1"))
Ver = "H2C1N0O1"
#print(Verbindung_einlesen(Verbingung))

print("neu")
#Verbindungen_Gewichtsprozent(Ver)
Ver="0.5 H1 + 0.25 C1 + 0.0 N1 + 0.25 O1"
print(Verbindungen_Gewichtsprozent(Ver))


