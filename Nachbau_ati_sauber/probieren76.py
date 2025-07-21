from Nachbau_ati_sauber.Element import Element
import numpy as np
#22.29   Ba
#20.00  Ta
#3.6    Zn


Ba_wert = 22.29
Ta_wert = 20
Zn_wert = 3.6

Ba = Element(Element="Ba")
Ta = Element(Element="Ta")
Zn = Element(Element="Zn")
O = Element(Element="O")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())

print(Ba_faktor,Ta_faktor,Zn_faktor)

Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])


#ohne Z 3.42 & 25.56 & 20.43

Ba_wert = 25.56
Ta_wert = 20.43
Zn_wert = 3.42


print("Ohne Z gemittelt")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())

print(Ba_faktor,Ta_faktor,Zn_faktor)

Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])
#beste z gemitt 3.49 & 23.61 & 19.63

Ba_wert = 23.87
Ta_wert = 19.04
Zn_wert = 3.18


print("beste z gemitt")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())

print(Ba_faktor,Ta_faktor,Zn_faktor)

Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])




Ba_wert = 0.41738236828377673
Ta_wert = 0.3973042205415955
Zn_wert = 0.06748488572130745


print("beste z gemitt")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())

print(Ba_faktor,Ta_faktor,Zn_faktor)

Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])

Ba_wert = 44.54
Ta_wert = 37.35
Zn_wert = 6.26


print("korrekteste")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())



Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])

Ba_wert = 43.32
Ta_wert = 36.26
Zn_wert = 6.07


print("korrekteste")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())



Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])


Ba_wert = 21.48
Ta_wert = 16.83
Zn_wert = 2.81


print("Geo=7")

Ba_faktor = 1 / Ba.Get_Atomicweight() * (Ba.Get_Atomicweight()+O.Get_Atomicweight())
Ta_faktor = 1 / Ta.Get_Atomicweight() * (Ta.Get_Atomicweight()+1.5*O.Get_Atomicweight())
Zn_faktor = 1 / Zn.Get_Atomicweight() * (Zn.Get_Atomicweight()+O.Get_Atomicweight())



Konz = np.array([Ba_wert*Ba_faktor, Ta_wert * Ta_faktor, Zn_wert*Zn_faktor])
print([kon / Konz.sum() for kon in Konz])
