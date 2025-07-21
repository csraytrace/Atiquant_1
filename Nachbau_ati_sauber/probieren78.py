from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *


Elemente = [(0, "O"),(6962, "Sr"), (3290, "Zr"), (3123, "Nb"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [0, 0, 0, 0, 0, 1, 1]

Verbindung="46.6 Ba1O1 + 45 Ta2O3 + 8.4 Zn1O1"

print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))
x,y,z=(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#P1=[8, 38, 40, 41, 30, 56, 1]

Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

Geo = 6.79137948809472e-06


Kon = [0.1067711,  0.00571978, 0.00228115, 0.00199023, 0.06291488, 0.4447184, 0.37560446]
Geo = 6.32805013e-06
#op_Konz, op_Geo = Ki.Minimierung_var_Geo(Geo, Z_Gewichtung=5, Startkonzentration=[0.1067711,  0.00571978, 0.00228115, 0.00199023, 0.06291488, 0.4447184, 0.37560446])
#print(op_Konz, op_Geo)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print("sollwerte",Konzentration)

op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=z,low_verteilung=[1])    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)
op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=30,low_verteilung=[1])    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)
#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(30,Startkonzentration=[0.1067711,  0.00571978, 0.00228115, 0.00199023, 0.06291488, 0.4447184, 0.37560446,6.79137948809472e-06])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(55.34,Startkonzentration=[0.1067711,  0.00571978, 0.00228115, 0.00199023, 0.06291488, 0.4447184, 0.37560446,6.79137948809472e-06])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(54,Startkonzentration=[0.1067711,  0.00571978, 0.00228115, 0.00199023, 0.06291488, 0.4447184, 0.37560446,6.79137948809472e-06])
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(54)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

print(P1)
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_mittelwert=z)
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=z,low_verteilung=[1])    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)
#print(np.array(normiere_daten(op_Konz))*2, op_Geo)
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_mittelwert=30)
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))



Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=z,low_verteilung=[1])    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)
