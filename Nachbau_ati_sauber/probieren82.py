from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Elemente = [(0, "O"), (29925, "Al")]
Übergänge = [0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#P1=[8, 38, 40, 41, 30, 56, 1]

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

op_Geo = 10**-6

op_Konz = [0,1]

x0 = (Ki.Intensität_alle_jit_fürMinimierung([0,1])[0]*op_Geo)
x20 = (Ki.Intensität_alle_jit_fürMinimierung([20,80])[0]*op_Geo)
x40 = (Ki.Intensität_alle_jit_fürMinimierung([40,60])[0]*op_Geo)
x60 = (Ki.Intensität_alle_jit_fürMinimierung([60,40])[0]*op_Geo)
x80 = (Ki.Intensität_alle_jit_fürMinimierung([80,20])[0]*op_Geo)
x90 = (Ki.Intensität_alle_jit_fürMinimierung([90,10])[0]*op_Geo)
print(x0,x20,x40,x60,x80,x90)
