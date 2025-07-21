import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

#K = Calc_I(Element_Probe=28, Konzentration=[3,3])
#K.Werte_vorbereiten_alle([12,13])
#print(K.Intensität_K())
#print(K.Intensität_K_alle())
#print(K.Intensität_K())

K = Calc_I(Element_Probe=30, Konzentration=[847554,477434], P1 = [29,30], Fensterdicke_det=12, Messzeit=300, Emax=30)


Geo = 4 * 10**-7 * 61 * 1.0066

print("start")

Ati_Konz = K.Intensität_alle_jit()


op_Konz = K.Minimierung_sqrt(Geo)
normiert_Konz = np.array([con / op_Konz.sum() for con in op_Konz])

print("counts mit NLLS", K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo)
print("relativer Unterschied NLLS", K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo / np.array([847554, 477434]))
print("Differenz NLLS", K.Intensität_alle_jit_fürMinimierung(op_Konz)[0] * Geo - np.array([847554, 477434]))


print("Kosten mit NLLS",K.Kosten(op_Konz, Geo))
print("Kosten mit NLLS normiert",K.Kosten(normiert_Konz, Geo))

print("Atiquant_normiert",K.Kosten(Ati_Konz, Geo))
print("Atiquant_skaliert",K.Kosten(np.array(Ati_Konz) * 10, Geo))

print("ende")


