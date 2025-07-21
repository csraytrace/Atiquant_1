import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

Geo = 4 * 10**-7 * 61 * 1.0066

K = Calc_I(Element_Probe=30, Konzentration=[847554,477434], P1 = [29,30], Fensterdicke_det=12, Messzeit=300, Emax=30,Übergänge=[1,1])
K = Calc_I(Element_Probe=30, Konzentration=[9362 ,847554,477434], P1 = [26 ,29,30], Fensterdicke_det=12, Messzeit=300, Emax=30)
#K = Calc_I(Element_Probe=30, Konzentration=[9362,8577 ,847554,477434], P1 = [26,28 ,29,30], Fensterdicke_det=12, Messzeit=300, Emax=30)

print(K.Übergänge)

#Ati_Konz = K.Intensität_K_alle_jit()


#op_Konz = K.Minimierung(Geo)
#normiert_Konz = np.array([con / op_Konz.sum() for con in op_Konz])

#op_Konz = K.Minimierung(Geo*1.1)

#print("Atiquantkonzentration",Ati_Konz)

