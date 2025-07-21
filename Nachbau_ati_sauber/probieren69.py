from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import Verbindung_einlesen, Filter

#, 'V1O2', 'V1', 'Bi1O3', 'BI1', 'Pb1O1', 'PB1', 'Ta1O5', 'TA1'

print(Filter("Si1", 3*10**-7, 1.74))
print(Filter("Si1O2", 3*10**-7, 1.74))
print(Filter("Si1O2", 1*10**-7, 1.74))


Verbindungen = ["Si1O2", "Si1", "Al2O3", "Al1", "Ti1O2", "Ti1"]
Verbindungen = ["Si1O2", "Si1", "Al2O3", "Al1",'Sn1O2', 'SN1', 'Ti1O2', 'Ti1', 'Cd1O1', 'CD1', 'Cu1O1', 'CU1',  'Zr1O2', 'ZR1', 'Zn1O1', 'ZN1', 'Ge1O2', 'GE1']
werte=[]
for Verbindung in Verbindungen:
    print(Verbindung_einlesen(Verbindung))

    Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=Verbindung_einlesen(Verbindung)[0], Konzentration=Verbindung_einlesen(Verbindung)[1])
    werte.append(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen(Verbindung)[1])[0][0])
    #print(werte[-1])


for i in range(len(werte)):
    if i%2==0:
        print(werte[i]/werte[i+1])

print(Verbindung_einlesen("Si1"))
print(Verbindung_einlesen("Al21O3"))
print(Verbindung_einlesen("Ti1O2"))


Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=Verbindung_einlesen("Pb")[0], Konzentration=Verbindung_einlesen("Pb")[1],Übergänge=[1])
x=(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen("Pb")[1])[0][0])

Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01,P1=Verbindung_einlesen("Pb1O1")[0], Konzentration=Verbindung_einlesen("Pb1O1")[1],Übergänge=[1,0])
y=(Ki.Intensität_alle_jit_fürMinimierung(Verbindung_einlesen("Pb1O1")[1])[0][0])
print("BleiO-L", y/x)
