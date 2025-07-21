import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files



#Calc = Calc_I(Messzeit = 30, Röhrenstrom= 0.01, Emax = 35, charzucont = 1, Fensterdicke_det=12)
#print(Calc.Geometriefaktor_ati_L(("cd", 9549)))
#print(Calc.Geometriefaktor_ati_L(("ag", 9783)))
#print(Calc.Geometriefaktor_ati_K(("ag", 31140)))


def BeerLambert(Massenschwachungskoe, Dichte, Dicke, Phi = 0):
    return np.exp(-Massenschwachungskoe * Dichte * Dicke / np.cos(Phi * np.pi / 180))

O = Element(Element="O")
N = Element(Element="N")
Ar = Element(Element="Ar")

Al = Element(Element="Al")
print(Al.K_gemittel_ubergang())
Si = Element(Element="Si")

Dichte = 1.2e-3 /100
Energie = Al.K_gemittel_ubergang()
Dicke = 3.5

Massenschwächungskoeffizient = O.Massenschwächungskoeffizient(Energie)[1] * 0.2094 + N.Massenschwächungskoeffizient(Energie)[1] * 0.78 + Ar.Massenschwächungskoeffizient(Energie)[1] * 0.0093

print(BeerLambert(Massenschwächungskoeffizient, Dichte, Dicke))
