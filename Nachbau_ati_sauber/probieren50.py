from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np
from probierenfunktionen import *


Elemente_auskunft(["Cu", "O", "H"])

K = Calc_I(Element_Probe=30, Konzentration=[1,1], P1 = ["H","Cu"], Messzeit=300, Emax=30)

#K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.1, 0.9])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.9, 0.1])[0])
#print(K.Intensität_K_alle_jit_fürMinimierung([1,1]))
Intensitäten(K.Intensität_alle_jit_fürMinimierung([1.0, 1.0])[0])

K = Calc_I(Element_Probe=30, Konzentration=[1,1,1], P1 = ["H","o","Cu"], Messzeit=300, Emax=30)
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.00, 0.00, 1.0])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.1, 0.00, 0.9])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.9, 0.00, 0.1])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.05, 0.05, 0.9])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.45, 0.45, 0.1])[0])

K = Calc_I(Element_Probe=30, Konzentration=[1,1,1], P1 = ["b", "Be","Cu"], Messzeit=300, Emax=30)
Elemente_auskunft(["b", "Be","Cu"])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.05, 0.05, 0.9])[0])
Intensitäten(K.Intensität_alle_jit_fürMinimierung([0.45, 0.45, 0.1])[0])
