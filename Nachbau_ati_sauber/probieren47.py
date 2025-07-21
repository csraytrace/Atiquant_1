from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np
from Nachbau_ati_sauber.Element import Element

def Ati_Geo(Intensitäten, P1):
    #print("IntfürGeo",Intensitäten[1:3], Intensitäten)
    neu_int = []
    neu_p1 = []
    for index, i in enumerate(Intensitäten):
        if i != 0:
            neu_int.append(i)
            neu_p1.append(P1[index])

    El = Calc_I(Element_Probe=30, Konzentration=neu_int, P1 = neu_p1, Messzeit=300, Emax=30)
    Konz = El.Intensität_alle_jit()
    #print(Konz)
    Int = (El.Intensität_alle_jit_fürMinimierung(Konz))
    for index,i in enumerate(Int):
        print(Intensitäten[index+1]/i)


P1 = [8,15,28]
#P1 = [8,12,40]
#P1 = [1,15,28]
K = Calc_I(Element_Probe=30, Konzentration=[0,0, 1], P1 = P1,Übergänge=[0,0,0], Messzeit=300, Emax=30)



#Z=21.4

Geo = 2.7151364588867653e-5
op_Konz = [0.5, 0.1, 0.40]
Intensität = ((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo))
Z_ge = sum(i* Element(Element=P1[index]).Get_Atomicnumber() for index, i in enumerate(op_Konz))
print("Ze_ge",Z_ge)
#Intensität = [0, 1.33602811e+06]
print(Intensität)
Ati_Geo(Intensität, P1)





K = Calc_I(Element_Probe=30, Konzentration=Intensität, P1 = P1,Übergänge=[0,0,0], Messzeit=300, Emax=30)
#K.Minimierung(Geo)
#K.Minimierung_res_neu(Geo)


#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*1.1)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*op_Geo).astype(int))

#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*0.9)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*op_Geo).astype(int))


#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*1.4)
op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*1.05, Z_Gewichtung=0.2, Z_gemittelt=Z_ge)
print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo))
print(Intensität)

op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*1, Z_Gewichtung=0.3, Z_gemittelt=Z_ge)
print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo))
print(Intensität)

op_Konz, op_Geo = K.Minimierung_var_Geo(Geo*0.95, Z_Gewichtung=0.4, Z_gemittelt=Z_ge)
print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo))
print(Intensität)

#op_Konz = K.Minimierung_relativ(Geo)
#print(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo)

#op_Konz = K.Minimierung_sqrt(Geo)
#print(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo)

#op_Konz = K.Minimierung_sqrt_zusatz(Geo)
#print(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo)
