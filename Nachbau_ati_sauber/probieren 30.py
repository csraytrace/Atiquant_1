from Nachbau_ati_sauber.Element import Element
import numpy as np
H = Element(Element = "o")
Mg = Element(Element = "mg")

print(H.Get_Elementsymbol())
print(Mg.Ubergange())

Energie = 1.255

print(H.Massenschwächungskoeffizient(Energie))
print(Mg.Massenschwächungskoeffizient(Energie))

print(0.9*H.Massenschwächungskoeffizient(Energie)[1] + 0.1 * Mg.Massenschwächungskoeffizient(Energie)[1])

print(1/Mg.Massenschwächungskoeffizient(Energie)[1])
print(1/(0.9*H.Massenschwächungskoeffizient(Energie)[1] + 0.1 * Mg.Massenschwächungskoeffizient(Energie)[1]))
li = np.array([1,2,3])
print(np.array(li))



