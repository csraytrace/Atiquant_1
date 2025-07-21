from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np

def Prozent(array):
    return (" & ".join([f"{value*100:.2f}" for value in array])+"\\\\")

H = Element(Element = "H")
O = Element(Element = "O")
S = Element(Element = "S")
Ce = Element(Element = "Ce")

Gesamtgewicht = Ce.Get_Atomicweight() + 2* S.Get_Atomicweight() + O.Get_Atomicweight() * 12 + H.Get_Atomicweight() * 8

H_Anteil = 8 * H.Get_Atomicweight() / Gesamtgewicht
O_Anteil = 12 * O.Get_Atomicweight() / Gesamtgewicht
S_Anteil = 2* S.Get_Atomicweight() / Gesamtgewicht
Ce_Anteil = Ce.Get_Atomicweight() / Gesamtgewicht


Gesamtgewicht_ceso = Ce.Get_Atomicweight() + S.Get_Atomicweight() + O.Get_Atomicweight() * 4
Gesamtgewicht_ho = O.Get_Atomicweight() * 4 + H.Get_Atomicnumber() * 8
print(H_Anteil,O_Anteil,S_Anteil,Ce_Anteil)
print(Gesamtgewicht)
print(H_Anteil+O_Anteil+S_Anteil+Ce_Anteil)




Geo = 2.7151364588867653e-05

Z_ge = H_Anteil * H.Get_Atomicnumber() + O_Anteil * O.Get_Atomicnumber() + S_Anteil * S.Get_Atomicnumber() + Ce_Anteil  * Ce.Get_Atomicnumber()
print("Zgemittelt", Z_ge)


#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[ 139924, 187433], P1 = ["S","ce"],Übergänge=[0,1], Messzeit=100, Emax=28, Röhrenstrom=0.02)
#op_Konz, op_Geo=K.Atiquant()
#print(op_Konz)
#print(op_Geo)
#print((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[0, 0, 139924, 187433], P1 = ["H","O","S","ce"],Übergänge=[0,0,0,1], Messzeit=100, Emax=28, Röhrenstrom=0.02)
#K = Calc_I(Element_Probe=30, Konzentration=[0, 0, 139924, 187433], P1 = ["H","O","S","ce"],Übergänge=[0,0,0,1], Messzeit=100, Emax=30, Röhrenstrom=0.02)



op_Konz, op_Geo = K.Minimierung_dark( Z_mittelwert=Z_ge,low_verteilung=[0.04,0.95])
print(op_Konz)
print(op_Geo)
print((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

op_Konz, op_Geo = K.Minimierung_dark( Z_mittelwert=23,low_verteilung=[0.04,0.95])
print(op_Konz)
print(op_Geo)
print((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))


print("Sollwerte", Prozent([H_Anteil, O_Anteil, S_Anteil, Ce_Anteil]))
print("sollintensitäten [0, 0, 139924, 187433]")
op_Konz = [H_Anteil,O_Anteil,S_Anteil,Ce_Anteil]
"""
#Geo =6.724129174442123e-05
#print((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))
#Geo =6e-05
#print((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))
Geo =7e-05
#print((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))
Int = ((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int))
print((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo * (139924 / Int[2])).astype(int))
Int = ((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int))
print((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo * (187433 / Int[3])).astype(int))

print(Geo * 187433/Int[3])
print(Geo * 139924/Int[2])
Geo *= (187433/Int[3]+139924/Int[2])/2
print(Geo)

#Geo =6.724129174442123e-05
#print((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))


#op_Konz = K.Minimierung(Geo)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))
#print("sollintensitäten [0, 0, 139924, 187433]")
#print("Sollwerte", H_Anteil, O_Anteil, S_Anteil, Ce_Anteil)

#Geo = 4.7151364588867653e-05
#op_Konz = K.Minimierung(Geo)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int))
#print("Sollwerte", H_Anteil, O_Anteil, S_Anteil, Ce_Anteil)

#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_Gewichtung=0.1,Z_gemittelt=Z_ge)
#print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo).astype(int))
#print("sollintensitäten [0, 0, 139924, 187433]")
#print("Sollwerte", Prozent([H_Anteil, O_Anteil, S_Anteil, Ce_Anteil]))

#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_Gewichtung=0.01,Z_gemittelt=Z_ge)
#print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo).astype(int))
#print("sollintensitäten [0, 0, 139924, 187433]")
#print("Sollwerte", Prozent([H_Anteil, O_Anteil, S_Anteil, Ce_Anteil]))

op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_Gewichtung=0.05,Z_gemittelt=Z_ge)
print("berechnete Intensitäten", (K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * op_Geo).astype(int))
print("sollintensitäten [0, 0, 139924, 187433]")
print("Sollwerte", Prozent([H_Anteil, O_Anteil, S_Anteil, Ce_Anteil]))
#Geo = 2.7151364588867653e-05
#print("dasselbe, anderer Startwert")
#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*op_Geo).astype(int))
#print("sollintensitäten [0, 0, 139924, 187433]")
#print("Sollwerte", H_Anteil, O_Anteil, S_Anteil, Ce_Anteil)


#K = Calc_I(activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[0, 0, 139924, 187433], P1 = ["H","O","S","ce"],Übergänge=[0,0,0,1], Messzeit=100, Emax=30, Röhrenstrom=0.02)
#op_Konz, op_Geo = K.Minimierung_var_Geo(Geo)
#print("berechnete Intensitäten",(K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*op_Geo).astype(int))
#print("sollintensitäten [0, 0, 139924, 187433]")
#print("Sollwerte", H_Anteil, O_Anteil, S_Anteil, Ce_Anteil)

for i in ["H","O","S","ce"]:
    x_Ele = Element(Element = i)
    print(x_Ele.Get_Elementsymbol(), x_Ele.Get_Atomicnumber())



"""
