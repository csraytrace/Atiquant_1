import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

x = Element(Element="22")
Energie = 40
print(x.Get_Elementsymbol())
print(x.Costa_Kronig())
print(x.Omega_Schale("L3"))
print(x.Omega())
print([float(i[1]) for i in x.Omega()])
print(x.Ubergange())
print(x.Massenabsorptionskoeffizient(Energie)[1]/x.Get_cm2g())
print(x.S_ij(" K", Energie))
print(x.S_ij("L1", Energie))
print(x.S_ij("L2", Energie))
print(x.S_ij("L3", Energie))

print(x.S_ij(" K", Energie) * x.Massenabsorptionskoeffizient(Energie)[1]/x.Get_cm2g())
print(x.S_ij("L1", Energie) * x.Massenabsorptionskoeffizient(Energie)[1]/x.Get_cm2g())
print(x.S_ij("L2", Energie) * x.Massenabsorptionskoeffizient(Energie)[1]/x.Get_cm2g())
print(x.S_ij("L3", Energie) * x.Massenabsorptionskoeffizient(Energie)[1]/x.Get_cm2g())

