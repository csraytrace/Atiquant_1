from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np

#Geo = 2.456104e-05
def formatted_output(values):
    return " & ".join(map(str, values)) + " \\\\"

Geo = 2.8e-05
Geo = 2.7151364588867653e-05
print("Geo:",Geo )

#K = Calc_I(Element_Probe=30, Konzentration=[850166, 478201], P1 = [29,30],Übergänge=[0,0], Messzeit=300, Emax=30)
#K = Calc_I(Element_Probe=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30) #'alt'
K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30) # neu


#op_Konz = K.Minimierung(Geo * Faktor)
op_Konz = K.Minimierung_sqrt(Geo)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt(Geo, Z_gemittelt=31.5125, Z_Gewichtung=0.1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt(Geo, Z_gemittelt=31.5125, Z_Gewichtung=5)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt(Geo, Z_gemittelt=31.5125, Z_Gewichtung=10)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))

op_Konz = K.Minimierung_sqrt_zusatz(Geo)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=0.1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=5)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=10)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))
#op_Konz = K.Minimierung_res_neu(Geo, Z_gemittelt=30, Z_Gewichtung=10)
#op_Konz = K.Minimierung_res_neu(Geo)


op_Konz = K.Minimierung_relativ(Geo)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))
op_Konz = K.Minimierung_relativ(Geo, Z_gemittelt=31.5125, Z_Gewichtung=0.1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))
op_Konz = K.Minimierung_relativ(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))
op_Konz = K.Minimierung_relativ(Geo, Z_gemittelt=31.5125, Z_Gewichtung=5)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))
op_Konz = K.Minimierung_relativ(Geo, Z_gemittelt=31.5125, Z_Gewichtung=10)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))

print("mein Gedanke")
Geo = 3.1e-05
#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))

op_norm = np.array([con /op_Konz.sum() for con in op_Konz])
print(op_Konz)
print(op_norm)
Z=0
P1 = [29,30]
#for index,con in enumerate(op_norm):
#    Z += con * P1[index]

print(Z)

for i in [26,28,29,30,50, 82]:
    x_Ele = Element(Element = i)
    print(x_Ele.Get_Elementsymbol())
