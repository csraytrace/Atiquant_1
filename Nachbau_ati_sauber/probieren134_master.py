import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre

Emin = 0
Emax = 40
step=0.01

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

#tube = Röhre(Emin=Emin,Emax=Emax,step=step, Einfallswinkelalpha=0,Einfallswinkelbeta=180)
tube = Röhre(Emin=Emin,Emax=Emax,step=step)
#x, y = tube.Gesamtspektrum_plot
x, y = tube.Röhrenspektrum
y/=0.01
plt.plot(x, y, color=colors[0], label=r"Wiederschwinger")

tube = Röhre(Emin=Emin,Emax=Emax,step=step,sigma=0.93925,Röhrenstrom=0.01*1.35/1.36)
#x, y = tube.Gesamtspektrum_plot
x, y = tube.Röhrenspektrum
y/=0.01
plt.plot(x, y, color=colors[3], label=r"Love und Scott")


#tube = Röhre(Emin=Emin,Emax=Emax,step=step)
#x, y = tube.Gesamtspektrum_plot
#plt.plot(x, y, color=colors[0], label=r"$\tau$ (gesamt)")

#plt.ylim(1, 10000)
plt.xlabel("Energie [keV]")
plt.ylabel(r"Intensität")
plt.yscale("log")
plt.title("Kontinuierliche Röhrenspektrum")
plt.ylim(10**9)
plt.legend(loc="upper right")
#plt.tight_layout()
#plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\KoninuierlichRöhre.png", dpi=1000, bbox_inches='tight')

plt.show()
