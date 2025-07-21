import cProfile
import pstats
import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element


Ele = Element(Element="cu")
L_Sn = Element(Element="sn")
#print(L_Sn.Kanten())
#plt.axvline(x=L_Sn.Kanten()[3][1], color='r', linestyle='-', label="sn-kante")

step = 0.001

tube = Röhre(step = step, Röhrenstrom=1, Emax = 40)
print(tube.Char_spec)

#print(tube.Countrate_gesamt)
start = int(000 * 0.0005 / step)
#start=0
for index, value in enumerate(tube.Röhrenspektrum[0]):
    if (value > Ele.Kanten()[0][1]):
        start2 = index
        break
    else:
        start2 = 0

#plt.plot(tube.Röhrenspektrum[0][start:], tube.Röhrenspektrum[1][start:], color="b", label=f"Röhre")
plt.plot(tube.Countrate_gesamt[0][start:], tube.Countrate_gesamt[1][start:], color="b", label=f"Rh-Röhrenspektrum")
plt.axvline(x=Ele.Kanten()[0][1], color='r', linestyle='-', label=Ele.Get_Elementsymbol()+'-K-Kante')

#plt.axvline(x=Ele.Ubergange()[0][1], color='gold', linestyle='-', label='K-L1')
if (Ele.Ubergange()[0][0] == " K-L1"):
    s = 0
else:
    s = -1

plt.axvline(x=Ele.Ubergange()[1+s][1], color='g', linestyle='-', label='K-L2')
print(Ele.Ubergange()[1+s][0])
plt.axvline(x=Ele.Ubergange()[2+s][1], color='purple', linestyle='-', label='K-L3')

plt.fill_between(tube.Röhrenspektrum[0][start2:], tube.Röhrenspektrum[1][start2:], color='orange', alpha=0.5, label='$\int_{E_{i\ j}}^{E_{max}} I_0 \,dE$')

#plt.xscale('log')
plt.yscale('log')
plt.title(r'Intensitätsberechung K$_\alpha$-'+Ele.Get_Elementsymbol())
plt.xlabel('Energie [keV]')
plt.ylabel('Intensität')


print(Ele.Kanten())
print(Ele.Ubergange())

plt.legend()
plt.show()


