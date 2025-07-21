from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Verbindung = "0.013 Al2O3 + 0.622 Ba1O1 + 0.028 Cr2O3 + 0.0002 Fe2O3 + 0.002 Si1O2 + 0.335 Ti1O2"
print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))
y = Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung)[1]
indices=[0,3,6]
print([y[i] for i in indices])

Elemente = [(0, "O"), (29925, "Ti"), (79790, "Ba")]
Übergänge = [0, 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
    #print(Element(Element=i[1]).Get_Atomicnumber())

#8,22,56

#Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht)
#print(Z_anpassen([0],[8], [0.11, 0.88],[22,56],37.9))
x,y =Z_anpassen([0],[8], [0.11, 0.88],[22,56],37.9)
x=x[0]
y=y[0]
#print(x+y)

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())

Startwerte = [x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
#print(Startwerte)
#print(P1)

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#Startwerte = [0, 0.11413267, 0.88586733, 4.73747169e-06]
#print(Startwerte)
#print(P1)

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))





Elemente = [(0, "O"), (29925, "Ti"), (13295, "Ba")]
Übergänge = [0, 0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())

Startwerte = [x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
#print(Startwerte)
#print(P1)

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


Elemente = [(0, "O"), (59343, "Ti"), (15637, "Ba")]
Übergänge = [0, 0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())

Startwerte = [x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
#print(Startwerte)
#print(P1)

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


Elemente = [ (59343, "Ti"), (15637, "Ba")]
Übergänge = [ 0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)
print(Ki.Atiquant())


