import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.Detektor import Detektor
import matplotlib.pyplot as plt
from numba import njit
from scipy.optimize import least_squares
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
from Nachbau_ati_sauber.Calc_I import Calc_I
import pandas as pd

"""

Ele = Element(Element="rh", Emin=5, Emax=10, step=1)
print(Ele.Massenschwächungskoeffizient_array())
print(Ele.Massenschwächungskoeffizient(24.44))
print(Ele.Kanten())

Det = Detektor()
energie = Det.Detektorspektrum()[0]
array = Det.Detektorspektrum()[1]
#for i in range(len(array)):
  #  print(energie[i],array[i])
tube = Röhre(step=5)
x,y =tube.Röhrenspektrum
for index, energie in enumerate(x):
    print(f"{energie:8.3f} | {y[index]:12.6e}")

#print(tube.Char_spec)
#print(tube.GetCountRateChar(20,5))


folder_path='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'
#print(Filter_array(Material="Ca", Dicke=0.001, Emin=3, Emax=10, step=1, Dateipfad=folder_path, Dichte = None, Fenstereinfallwinkel=0))
#print(Filter_array(Material="air", Dicke=1, Emin=10, Emax=40, step=10, Dateipfad=folder_path, Dichte = None, Fenstereinfallwinkel=0))
print(Filter_array(Material="Cu", Dicke=0.001, Emin=5, Emax=40, step=5, Dateipfad=folder_path, Dichte = None, Fenstereinfallwinkel=0))
#print(Filter_array(Material="Cu", Dicke=0.01, Emin=10, Emax=40, step=10, Dateipfad=folder_path, Dichte = None, Fenstereinfallwinkel=0))

#print(Filter(Material="1 Cu", Dicke=0.01, Energie=20, Dichte = None, Fenstereinfallwinkel=0))


Ki = Calc_I(Konzentration=[1], P1=["rh"], Übergänge=[0], Emax=30,step=10)
print("vorbereitet Werte")
print(Ki.Werte_vorbereiten_alle_jit())

# ------------------------------------------------------------
# 1. Werte holen
# ------------------------------------------------------------
(
    palpha, pbeta, tube0, tau0, omega0, mu0, sij0, tau, mu, countrate,
    mu_ijk, det_ijk, sij, alle_kanten, alle_ueberg, sij_xyz, tau_ijk,
    konzentration, step, emin, ltf
) = Ki.Werte_vorbereiten_alle_jit()

# ------------------------------------------------------------
# 2. Schön ausgeben
# ------------------------------------------------------------
def headline(txt):
    print(f"\n\033[1m{txt}\033[0m")          # fett

headline("Allgemeine Parameter")
print(f"  • Pα              : {palpha:10.6f}")
print(f"  • Pβ              : {pbeta:10.6f}")
print(f"  • step            : {step}")
print(f"  • Emin            : {emin}")
print(f"  • Konzentrationen : {konzentration}")

headline("Countrate (Spektrum)")
print(pd.Series(countrate).head(10))         # nur die ersten 10 Kanäle

headline("Tube0 (nEle × 4)")
print(pd.DataFrame(tube0))

headline("Ω0 (nEle × 4)")
print(pd.DataFrame(omega0))

headline("Übergänge (nEle × mau × 3)")
print("Shape:", alle_ueberg.shape)
print("Beispiel Element 0:")
print(pd.DataFrame(alle_ueberg[0], columns=["Code", "E [keV]", "Whs"]))

# ------------------------------------------------------------
# 3. Optional – alles als NPZ speichern
# ------------------------------------------------------------
np.savez_compressed(
    "prepared_values.npz",
    palpha=palpha, pbeta=pbeta, tube0=tube0, tau0=tau0, omega0=omega0,
    mu0=mu0, sij0=sij0, tau=tau, mu=mu, countrate=countrate,
    mu_ijk=mu_ijk, det_ijk=det_ijk, sij=sij, alle_kanten=alle_kanten,
    alle_ueberg=alle_ueberg, sij_xyz=sij_xyz, tau_ijk=tau_ijk,
    konzentration=konzentration, step=step, emin=emin, ltf=ltf
)
print("\nAlle Daten komprimiert in 'prepared_values.npz' gespeichert.")
"""
Ki = Calc_I(Konzentration=[2,1], P1=["si","al"], Übergänge=[0,0], Emax=30,step=10)
x = Ki.Intensität_alle_jit()
print(Ki.Atiquant())
print("X",x)
#x.tolist()
print(Ki.Intensität_alle_jit_fürMinimierung(x))

"""



          #     Verbindung v1 = f.parseFormelMitNormierung("CaCO3 4",0.25, 2.25, 0.5, "McMaster.txt"); // z.B. CaCO3
         #   Verbindung v2 = f.parseFormelMitNormierung("MgCO3 2",0.25, 2.25, 0.5, "McMaster.txt");

print(Verbindungen_Gewichtsprozent_vonMassenprozent("2 Ca1C1O3 + 3 Mg1C1O3"))

z,c,ir = Verbindungen_Gewichtsprozent_vonMassenprozent("2 Ca1C1O3 + 3 Mg1C1O3")

liste = np.zeros(len(Element(Element="h",Emin=0.25,Emax=2.25,step=0.5).Massenabsorptionskoeffizient_array()[1]))
for i, ele in enumerate(z):
    x_ele = Element(Element=ele,Emin=0.25,Emax=2.25,step=0.5)
    liste += x_ele.Massenschwächungskoeffizient_array()[1] * c[i]

print(liste)
print(x_ele.Massenschwächungskoeffizient_array()[0])
print(Element(Element="Mg",Emin=0.25,Emax=2.25,step=0.5).Massenabsorptionskoeffizient_array()[1])
#print(Verbindungen_Gewichtsprozent("1 Ca1C1O3"))
#print(Gewichtsprozent_Atomprozent("1 Ca1O2"))

#print(Verbindung_einlesen("Ca1C1O3"))

#Det = Detektor()
#spk=Det.Detektorspektrum()
#for i in range(1, 95):
 #   #x=Element(Element="1")
 #   x=Element(Element=str(i))
 #   print(str(x.Get_Elementsymbol())+",")
    #if len(x.Get_Elementsymbol())<2: print(x.Get_Elementsymbol())
"""
