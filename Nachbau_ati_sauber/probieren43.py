from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np
def formatted_output(values):
    return " & ".join(map(str, values)) + " \\\\"

Geo = 2.71662657e-05
#K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
#op_Konz = K.Minimierung_anders(Geo)
def formatted_output(values):
    return " & ".join(map(str, values)) + " \\\\"


K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)
#op_Konz = K.Minimierung_var_Geo(2.71662657e-05)
#print("berechnete Intensitäten",formatted_output((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo).astype(int)))


op_Konz, op_Geo = K.Minimierung_var_Geo(Geo)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * op_Geo).astype(int)))
op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_gemittelt=31.5125, Z_Gewichtung=0.05)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * op_Geo).astype(int)))
op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_gemittelt=31.5125, Z_Gewichtung=0.1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * op_Geo).astype(int)))
op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * op_Geo).astype(int)))
op_Konz, op_Geo = K.Minimierung_var_Geo(Geo, Z_gemittelt=31.5125, Z_Gewichtung=5)
print("berechnete Intensitäten", formatted_output((K.Intensität_alle_jit_fürMinimierung(op_Konz) * op_Geo).astype(int)))
