import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

#Elementliste = []
#Elementliste.append(Element(Element="Ag"))
#Elementliste.append(Element(Element="si"))

#print(Elementliste)
#print(Elementliste[1].Get_Elementsymbol())

print(len((4,3,2)))

def Probeneingabe(Probe):
    if (isinstance(Probe, int)):
        return [Probe]
    if (isinstance(Probe, list)):
        return Probe
    try:
        Länge = len(Probe)
    except:
        print("Probe nicht richtig beschrieben")
    if (Länge <=2) and isinstance(Probe, str):
        return [Probe]
    if (isinstance(Probe, tuple)):
        return [i for i in Probe]



print(Probeneingabe(["si", 23]))
print(Probeneingabe(("si", 23)))
print(Probeneingabe(23))
print(Probeneingabe(["si"]))
print(Probeneingabe(("si", 34,24, "se")))
x=23

