import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

ele = "pb"
P = Element(Element = ele)
print(P.Get_Atomicnumber())
#print(P.Get_Elementsymbol())

#print(sum(P.Costa_Kronig()))
#print(Ph.Daten)
#print(P.Kanten())
#print(P.Löcherübertrag_L3(4))
#for i in range(40):
    #print(P.Löcherübertrag_L3_Energie(i))
#def Löchertransfer_L3(Kanten, Energie)
#print(P.Löcherübertrag())
Int = Calc_I(Element_Probe=ele)
print(Int.Intensität_K())
#print(Int.Intensität_L())
#print(P.Löcherübertrag())
#print(P.Massenschwächungskoeffizient_array())
print(P.Kanten())
#for i, v in enumerate(P.Löcherübertrag()[4]):
    #if (v!=1):
        #print(v, P.Löcherübertrag()[0][i])
print(P.Löcherübertrag_L3_Energie(3.55))


