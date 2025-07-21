import numpy as np


from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *


binder=([0.25,0.5,0.25],["1 H1C1O1","1 h1"])
print(binder[1])
print(Verbindungen_Gewichtsprozent_vonMassenprozent(binder[1][0]))
#print(Verbindungen_Gewichtsprozent_vonMassenprozent("1C38H76N2O2"))



Elemente = [(0,"H"), (0,"N"),(0,"O"),       (9302,"Al"), (59419,"Si"),(16117,"K"), (288300,"Ca"), (0,"C"), (9484,"Ti"), (7276,"Mn"), (206950,"Fe"), (7015,"Zn"), (9340,"As"),(14433,"Rb"), (19324,"Sr")]    #Mg????, (3000,"Mg")
Übergänge = [0,0,0,0,    0,0, 0, 0,   0,0, 0, 0,    0,0, 0]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])


Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low(Z_mittelwert=10,low_verteilung=[0,0,1,0],binder=binder)



Verbindung = []

#print(Verbindung_einlesen("H2O1"))
#print(Verbindungen_Gewichtsprozent("1 H2O1"))
#print(Verbindungen_Gewichtsprozent_vonMassenprozent("1H2 + 1O1"))

#Verbingung="H2O1"
#if Verbingung[0].isdigit():
 #   print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbingung))
#else:
#    print(Verbindungen_Gewichtsprozent_vonMassenprozent("1"+Verbingung))

#([1,1,1],["1 H1O1", "2 He1O1 + 4 C1O4"])
#print(Verbindungen_Gewichtsprozent_vonMassenprozent("1 C1O4 + 2 He1"))
print(Verbindungen_Gewichtsprozent_vonMassenprozent("4 C1O4"))
print(np.array(Verbindungen_Gewichtsprozent_vonMassenprozent("4 C1O4")[1])*0.5)
print(np.array(Verbindungen_Gewichtsprozent_vonMassenprozent("4 H2O1")[1])*0.5)

def Sym_Z(array):
    z=[]
    for i in array:
        z.append(Element(Element=i).Get_Atomicnumber())
    return z

print(Sym_Z(Verbindungen_Gewichtsprozent_vonMassenprozent("4 C1O4")[0]))


import numpy as np

# Erstes Array mit allen Zahlen
array1 = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])

# Zweites Array mit Zahlen, deren Indizes im ersten Array gesucht werden
array2 = np.array([70, 50, 90])  # Diese Werte sollen gefunden werden

# Indizes der Werte aus array2 in array1 (sortiert wie array2)
indices = np.array([np.where(array1 == val)[0][0] for val in array2])

print("Indizes in der richtigen Reihenfolge:", indices)

