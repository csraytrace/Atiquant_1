from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Elemente = [ (29925, "Ti"), (79790, "Ba")]
Übergänge = [ 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

x,y =Z_anpassen([0,0],[1,8], [0.11, 0.88],[22,56],37.9)
print(x,y)


Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

Ki.Atiquant()
op_Konz=[0.11413267, 0.88586733]
a,b=Ki.Intensität_alle_jit_fürMinimierung(op_Konz)
#print(a*4.737471694547475e-06)
#print(a*4.445708366157883e-06)

Elemente = [(0,"H"),(0, "O"), (29925, "Ti"), (79790, "Ba")]
Übergänge = [0,0, 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

x,y =Z_anpassen([0],[8], [0.11, 0.88],[22,56],37.9)



Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

#print(Ki.Atiquant())

Startwerte = [0,x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
Startwerte = [0,x, 0.11413267*y, 0.88586733*y, 1]
#print(Startwerte)
#print(P1)

#Ki.Minimierung_var_Geo_Ati(37.89)

Ki.Minimierung_dark(37.89,[1,1])
Ki.Minimierung_dark(37.89,[0,1])
Ki.Minimierung_dark(37.89,[1,0])

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
#x1,y1 = ((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)))
#print(x1*op_Geo)




#Startwerte = [x,0, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
#print(Startwerte)
#print(P1)

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
#x,y = ((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)))
#print(x*op_Geo)
#print(y)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

"""
Startwerte = [x,0, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

Startwerte = [x,x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
Startwerte = [x,4*x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


Startwerte = [4*x,x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Startwerte)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
"""
