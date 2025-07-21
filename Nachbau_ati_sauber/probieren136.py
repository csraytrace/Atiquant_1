import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor

Emin = 0
Emax = 40
step=0.01

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

#tube = Röhre(Emin=Emin,Emax=Emax,step=step, Einfallswinkelalpha=0,Einfallswinkelbeta=180)
det = Detektor(Emin=Emin,Emax=Emax,step=step)
#x, y = tube.Gesamtspektrum_plot
x, y = det.Detektorspektrum()

plt.plot(x, y, color=colors[0], label=r"Detektoreffizienz")



#tube = Röhre(Emin=Emin,Emax=Emax,step=step)
#x, y = tube.Gesamtspektrum_plot
#plt.plot(x, y, color=colors[0], label=r"$\tau$ (gesamt)")

#plt.ylim(1, 10000)
plt.xlabel("Energie [keV]")
plt.ylabel(r"Detektoreffizienz")
#plt.yscale("log")
plt.title("Simulation der Detektoreffizienz")
#plt.ylim(10**9)
#plt.legend(loc="upper right")
#plt.tight_layout()
plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Detektoreffizienz.png", dpi=1000, bbox_inches='tight')

plt.show()
