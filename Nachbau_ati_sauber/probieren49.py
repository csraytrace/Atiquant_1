from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np
from Nachbau_ati_sauber.Element import Element


#P1 = [1,"Cu"]
#K = Calc_I(Element_Probe=30, Konzentration=[0, 1], P1 = P1,Übergänge=[0,0], Messzeit=300, Emax=30)

#print(K.Intensität_K_alle_jit_fürMinimierung([0,1]))
#print(K.Intensität_K_alle_jit_fürMinimierung([0.99,0.01]))
#for i in P1:
#    print(Element(Element=i).Get_Elementsymbol(),Element(Element=i).Get_Atomicnumber())
#Z=21.4
H = Element(Element = "H")
O = Element(Element = "O")
S = Element(Element = "S")
Ce = Element(Element = "Ce")

Gesamtgewicht = Ce.Get_Atomicweight() + S.Get_Atomicweight() + O.Get_Atomicweight() * 8 + H.Get_Atomicweight() * 8

H_Anteil = 8 * H.Get_Atomicweight() / Gesamtgewicht
O_Anteil =  8 * O.Get_Atomicweight() / Gesamtgewicht
S_Anteil = S.Get_Atomicweight() / Gesamtgewicht
Ce_Anteil = Ce.Get_Atomicweight() / Gesamtgewicht

Geo = 2.7151364588867653e-05

Z_ge = H_Anteil * H.Get_Atomicnumber() + O_Anteil * O.Get_Atomicnumber() + S_Anteil * S.Get_Atomicnumber() + Ce_Anteil * Ce.Get_Atomicnumber()
print("Zgemittelt", Z_ge)
op_Konz = [H_Anteil,O_Anteil,S_Anteil,Ce_Anteil]
print(H_Anteil,O_Anteil,S_Anteil,Ce_Anteil)


Gesamtgewicht_ceso = Ce.Get_Atomicweight() + S.Get_Atomicweight() + O.Get_Atomicweight() * 4
Gesamtgewicht_ho = O.Get_Atomicweight() * 4 + H.Get_Atomicnumber() * 8

H_Anteil = 8 * H.Get_Atomicweight() / Gesamtgewicht_ho
O_Anteil =  4 * O.Get_Atomicweight() / Gesamtgewicht_ho + 4 * O.Get_Atomicweight() / Gesamtgewicht_ceso
S_Anteil = S.Get_Atomicweight() / Gesamtgewicht_ceso
Ce_Anteil = Ce.Get_Atomicweight() / Gesamtgewicht_ceso
print(H_Anteil,O_Anteil,S_Anteil,Ce_Anteil)
Geo = 2.7151364588867653e-05

Z_ge = H_Anteil * H.Get_Atomicnumber() + O_Anteil * O.Get_Atomicnumber() + S_Anteil * S.Get_Atomicnumber() + Ce_Anteil  * Ce.Get_Atomicnumber()
print("Zgemittelt", Z_ge)
