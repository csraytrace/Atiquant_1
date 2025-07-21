import numpy as np


from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *


Verbindung = "47000 Al + 163000 Ca + 25700 Fe + 12100 K + 11300 Mg + 2400 Na + 180000 Si + 3000 Ti + 631 Mn + 51 Rb + 108 Sr + 104 Zn + 13.4 As"
print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

print(Verbindungen_Gewichtsprozent_vonMassenprozent("0.5 H + 2.0 O + 0.0 N + 1.5 C"))


zahlen = np.array([0.5, 0.1, 0, 2])
strings = np.array(["H", "O", "N", "C"])

# Kombiniere die Werte mit einer zusätzlichen "1" nach jedem Element
kombiniert = " + ".join(f"{z} {s}1" for z, s in zip(zahlen, strings))

print(kombiniert)
print(Verbindungen_Gewichtsprozent_vonMassenprozent(kombiniert))
print(Verbindungen_Gewichtsprozent(kombiniert))



