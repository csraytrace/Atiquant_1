from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import Verbindung_einlesen

Geo = 4 * 10**-7 * 61 * 1.0066

print("Probeneingabe",Verbindung_einlesen("fe2o5si1"))
#k1 = x
#k2 = 1-x
#k1 * Fe2O3 + k2 * SiO2
Atomgewichte = []

O = Element(Element = 8)
Si = Element(Element = 14)
Fe = Element(Element = 26)

k1 = 0.5    #Konzentration 1

Eisenanteil = k1 * (Fe.Get_Atomicweight()*2/(Fe.Get_Atomicweight()*2+O.Get_Atomicweight()*3))
Sauerstoffanteil = k1 * (O.Get_Atomicweight()*3/(Fe.Get_Atomicweight()*2+O.Get_Atomicweight()*3))
#print(Eisenanteil,Sauerstoffanteil)
Sianteil = (1-k1) * (Si.Get_Atomicweight()/(Si.Get_Atomicweight()+O.Get_Atomicweight()*2))
Si_Sauerstoff = (1-k1) * (O.Get_Atomicweight()*2/(Si.Get_Atomicweight()+O.Get_Atomicweight()*2))
#print(Sianteil, Si_Sauerstoff)
print("Fe:", Eisenanteil, "Si:", Sianteil, "O:", Si_Sauerstoff+Sauerstoffanteil)


#K = Calc_I(Element_Probe=30, Konzentration=[847554,477434], P1 = [29,30], Fensterdicke_det=12, Messzeit=300, Emax=30)
K = Calc_I(Element_Probe=30, Konzentration=[0,847554,477434], P1 = [8,14,26], Messzeit=300, Emax=30)



#print(K.Intensität_K_alle_jit_fürMinimierung([0.65360216, 0.34639784])*Geo)
#print(K.Intensität_K_alle_jit_fürMinimierung([0.20,0.65360216, 0.34639784])*Geo)

neu_Konz = np.array([Si_Sauerstoff+Sauerstoffanteil,Sianteil,Eisenanteil])
normiert_Konz = np.array([con / neu_Konz.sum() for con in neu_Konz])

print("exakte_Konzentration",normiert_Konz)


neue_Intensität = K.Intensität_alle_jit_fürMinimierung(normiert_Konz)[0] * Geo
print("neuen_Intensitäten",neue_Intensität)

K = Calc_I(Element_Probe=30, Konzentration=neue_Intensität, P1 = [8,14,26], Messzeit=300, Emax=30)

#neue_Intensität[2] *=1.05
#neue_Intensität[1] *=0.95
op_Konz = K.Minimierung_sqrt(Geo)
neue_Intensität[0]=0
#neue_Intensität[1]=0
print("neuen_Intensitäten",neue_Intensität)
K = Calc_I(Element_Probe=30, Konzentration=neue_Intensität, P1 = [8,14,26], Messzeit=300, Emax=30)

#neue_Intensität[2] *=1.05
#neue_Intensität[1] *=0.95
op_Konz = K.Minimierung_relativ(Geo)
