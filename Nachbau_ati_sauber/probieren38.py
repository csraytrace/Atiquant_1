from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np

#Geo = 2.456104e-05
Faktor = 1

def formatted_output(values):
    return " & ".join(map(str, values)) + " \\\\"


K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)
K.Intensität_alle_jit()

Geo = 2.4e-05
print("Geo:",Geo * Faktor)
op_Konz = K.Minimierung_sqrt(Geo * Faktor)
#op_Konz = K.Minimierung_res_neu(Geo * Faktor)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo).astype(int)))

Geo = 2.6e-05
print("Geo:",Geo * Faktor)
op_Konz = K.Minimierung_sqrt(Geo * Faktor)
#op_Konz = K.Minimierung_res_neu(Geo * Faktor)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))

Geo = 2.8e-05
print("Geo:",Geo * Faktor)
op_Konz = K.Minimierung_sqrt(Geo * Faktor)
#op_Konz = K.Minimierung_res_neu(Geo * Faktor)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo).astype(int)))



#Geo = 2.4e-05
#print("Geo:",Geo * Faktor)

#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung(Geo * Faktor)
#op_Konz = K.Minimierung(Geo * Faktor)

#Geo = 2.6e-05
#print("Geo:",Geo * Faktor)

#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung(Geo * Faktor)
#op_Konz = K.Minimierung(Geo * Faktor)

#Geo = 2.8e-05
#print("Geo:",Geo * Faktor)

#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung(Geo * Faktor)
#op_Konz = K.Minimierung(Geo * Faktor)

#Geo = 3e-05
#print("Geo:",Geo * Faktor)

#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung(Geo * Faktor)
#op_Konz = K.Minimierung(Geo * Faktor)

#Geo = 3.1e-05
#print("Geo:",Geo * Faktor)

#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung(Geo * Faktor)
#op_Konz = K.Minimierung(Geo * Faktor)




print(K.Intensität_alle_jit_fürMinimierung(op_Konz) * Geo * Faktor)
print()
for i in [26,28,29,30,50, 82]:
    x_Ele = Element(Element = i)
    print(x_Ele.Get_Elementsymbol())

