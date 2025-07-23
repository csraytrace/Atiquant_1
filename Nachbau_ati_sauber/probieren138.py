import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor

Emin = 1
Emax = 1000
step=0.01

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

#tube = Röhre(Emin=Emin,Emax=Emax,step=step, Einfallswinkelalpha=0,Einfallswinkelbeta=180)
ele = Element(Emin=Emin,Emax=Emax,step=step,Element="Cu")
#x, y = tube.Gesamtspektrum_plot
x, y = ele.Massenabsorptionskoeffizient_array()
x, y1 = ele.Massenschwächungskoeffizient_array()
x, y2 = ele.Tau_coh()
x, y3 = ele.Tau_incoh()

plt.plot(x, y, color=colors[0], label=r"$\tau$ Massenabsorptionskoeffizient")
plt.plot(x, y1, color=colors[1], label=r"$\mu$ Massenschwächungskoeffizient")
plt.plot(x, y2, color=colors[2], label=r"$\sigma_\mathrm{coh} $ elastische Streuung")
plt.plot(x, y3, color=colors[3], label=r"$\sigma_\mathrm{inc}$ inelastische Streuung")



#tube = Röhre(Emin=Emin,Emax=Emax,step=step)
#x, y = tube.Gesamtspektrum_plot
#plt.plot(x, y, color=colors[0], label=r"$\tau$ (gesamt)")

#plt.ylim(1, 10000)
plt.xlabel("Energie [keV]")
plt.ylabel(r"$\left[\frac{\mathrm{cm}^2}{\mathrm{g}}\right]$")
plt.xscale("log")
plt.yscale("log")
plt.title("Schwächungskoeffizienten von Cu")
#plt.ylim(10**9)
plt.legend(loc="upper right")
#plt.tight_layout()
plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Schwächungskoeffizienten_1.png", dpi=300, bbox_inches='tight')

plt.show()
