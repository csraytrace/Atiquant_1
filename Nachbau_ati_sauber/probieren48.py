from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np
from Nachbau_ati_sauber.Element import Element





P1 = [8,15,28]
K = Calc_I(Element_Probe=30, Konzentration=[0,0, 1], P1 = P1,Übergänge=[0,0,0], Messzeit=300, Emax=30)

def Ati_Geo(Intensitäten):
    #print("IntfürGeo",Intensitäten[1:3], Intensitäten)
    El = Calc_I(Element_Probe=30, Konzentration=Intensitäten[1:3], P1 = P1[1:3],Übergänge=[0,0], Messzeit=300, Emax=30)
    Konz = El.Intensität_alle_jit()
    print(Konz)
    Int = (El.Intensität_alle_jit_fürMinimierung(Konz)[0])
    for index,i in enumerate(Int):
        print(Intensitäten[index+1]/i)


#Konz = K.Intensität_alle_jit()
#x = (K.Intensität_K_alle_jit_fürMinimierung(Konz))
#for index,i in enumerate(x):
#    print(Konzentration[index]/i)
#Z=21.4

Geo = 2.7151364588867653e-5

op_Konz = [0.30, 0.1, 0.60]
Intensität = ((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo))
Z_ge = sum(i* Element(Element=P1[index]).Get_Atomicnumber() for index, i in enumerate(op_Konz))
for i in P1:
    print(Element(Element=i).Get_Elementsymbol())
print("Ze_ge",Z_ge)
#Intensität = [0, 1.33602811e+06]
print(Intensität)

op_Konz = np.array([0.30, 0.2, 0.2])
for i in np.arange(0, 1.1, 0.1):
    op_Konz[0]=i
    print("Konzentartionen", np.array([con / op_Konz.sum() * 100 for con in op_Konz]))
    Intensität = ((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo))
    Ati_Geo(Intensität)
    #print(Intensität)


#Konz = K.Intensität_alle_jit()
#x = (K.Intensität_K_alle_jit_fürMinimierung(Konz))
#for index,i in enumerate(x):
#    print(Konzentration[index]/i)



