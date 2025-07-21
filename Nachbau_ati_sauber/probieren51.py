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



step = 0.05

tube = Röhre(step = step, Röhrenstrom=1, Emin=1.126,Emax = 25)
print(tube.Char_spec)
print(tube.Countrate_gesamt)
plt.plot(tube.Countrate_gesamt[0], tube.Countrate_gesamt[1], color="b", label=f"Rh-Röhrenspektrum")

#plt.xscale('log')
plt.yscale('log')
plt.xlabel('Energie [keV]')
plt.ylabel('Intensität')



plt.legend()
plt.show()


