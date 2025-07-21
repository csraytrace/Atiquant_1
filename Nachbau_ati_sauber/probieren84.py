from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *



print(Filter(Material="Luft", Dicke=1, Energie=1.74, Dichte = None, Fenstereinfallwinkel=0))
print(Filter(Material="Luft", Dicke=0.5, Energie=1.74, Dichte = None, Fenstereinfallwinkel=0))
print(Filter(Material="Luft", Dicke=1.5, Energie=1.74, Dichte = None, Fenstereinfallwinkel=0))

Elemente = [(0,"H"),(0, "O"), (29925, "Ti"), (79790, "Ba")]
Übergänge = [0,0, 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

print("Intensitäten",Konzentration)

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)


#Ki.Minimierung_var_Geo_Ati(37.89)
#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[0,1])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[0,1], Startkonzentration=[18.64 , 10.65 , 8.07 , 62.63,4.84e-06*1.1])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,0])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,0])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
op_Konz1, op_Geo1 = op_Konz, op_Geo


#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],Startkonzentration=[10.87 , 19.66 , 7.93 , 61.54 , 4.93e-06 *(1.03)])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],Startkonzentration=[23.79 , 4.68 , 8.16 , 63.36 , 4.78e-06*(1.03)])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#for i in np.arange(0.02,0.14,0.02):
   # print(i)
    #op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],Startkonzentration=[23.79 , 4.68 , 8.16 , 63.36 , 4.78e-06*(0.94+i)])
    #op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],Startkonzentration=[10.87 , 19.66 , 7.93 , 61.54 , 4.93e-06 *(0.94+i)])
    #print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print("dark")
Ki.Minimierung_dark( Z_mittelwert=37.89,low_verteilung=[0,1])
Ki.Minimierung_dark( Z_mittelwert=37.89,low_verteilung=[1,0])
Ki.Minimierung_dark( Z_mittelwert=37.89,low_verteilung=[1,1])
print("darkende")


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=37.89,low_verteilung=[0,1])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=37.89,low_verteilung=[1,0])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

print()



op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=37.89,low_verteilung=[1,1])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

Start = np.append(op_Konz, op_Geo)
Start=Start.tolist()
print("verschönern")


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Start)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=37.89,low_verteilung=[30,70])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

Start = np.append(op_Konz, op_Geo)
Start=Start.tolist()

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Start)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=37.89,low_verteilung=[70,30])
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

Start = np.append(op_Konz, op_Geo)
Start=Start.tolist()

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Startkonzentration=Start)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))





#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[0,1],low_fix=[0,1], fix_bounds=0.3)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,0],low_fix=[1,0], fix_bounds=0.3)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],low_fix=[1,1], fix_bounds=1)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89,Verteilung=[1,1],low_fix=[1,1], fix_bounds=0.2)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)

print("willhaben")
#print(Ki.Intensität_alle_jit_fürMinimierung([0.0,32.25,7.74,60.01])[0]*5.0537437154865966e-06)

Elemente = [(0, "O"), (29925, "Ti"), (79790, "Ba")]
Übergänge = [0, 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])



#Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)


#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Geo)



Elemente = [(0, "O"), (29925, "Ti"), (79790, "Ba")]
Übergänge = [0, 0, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

print("Intensitäten",Konzentration)

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)



op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(37.89)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz1[1:])[0]*op_Geo1))

