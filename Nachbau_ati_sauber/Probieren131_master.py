import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element

Emin = 0.2
Emax = 120
step=0.01

x_ele = Element(Element="Pb", step=step, Emax=Emax, Emin=Emin)
x, y = x_ele.Massenabsorptionskoeffizient_array()

K = np.array([x_ele.TauK(xi) for xi in x])
L1 = np.array([x_ele.TauL(xi) for xi in x])
L2 = np.array([x_ele.TauM(xi) for xi in x])
L3 = np.array([x_ele.TauN(xi) for xi in x])

colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

#plt.figure(figsize=(8, 5))

#plt.plot(x, K,     color=colors[2], label=r"$\tau$ (gesamt)")
plt.plot(x, L1,     color=colors[2], label=r"$\tau$ - $\tau_K$")
plt.plot(x, L2,     color=colors[3], label=r"$\tau$ - $\tau_K$ - $\tau_{L}$")
plt.plot(x, L3,     color=colors[4], label=r"$\tau$ - $\tau_K$ - $\tau_{L}$ - $\tau_{M}$")
plt.plot(x, y,      color=colors[0], label=r"$\tau$ (gesamt)")

#plt.ylim(1, 10000)
plt.xlabel("Energie [keV]")
plt.ylabel(r"$\tau$")
plt.yscale("log")
plt.title("Pb Massenabsorptionskoeffizient")

plt.legend(loc="upper right")
#plt.tight_layout()
#C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Pb_Massenabsorptionskoeffizient_ganz.png
plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Pb_Massenabsorptionskoeffizient_ganz.png", dpi=600, bbox_inches='tight')
#plt.savefig("Pb_Massenabsorptionskoeffizient_ganz.png", dpi=600, bbox_inches='tight')
plt.show()
