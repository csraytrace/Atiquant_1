from Nachbau_ati_sauber.Element import Element
import matplotlib.pyplot as plt
import numpy as np

coh = []
inc = []
x = list(range(1, 95))  # Ordnungszahlen 1 bis 100
#Energie=40
Energie=20.2
#Energie=2.7
for i in x:
    print(i)
    x_ele = Element(Element=str(i))
    inc.append(x_ele.Tau_incoh_energie(Energie))  # inkohärent (Compton)
    coh.append(x_ele.Tau_coh_energie(Energie))    # kohärent (Rayleigh)

plt.plot(x, coh, label="Rayleigh (kohärent)")
plt.plot(x, inc, label="Compton (inkohärent)")
plt.plot(x, np.array(inc)/np.array(coh), label="R")
plt.xlabel("Ordnungszahl Z")
plt.yscale("log")
plt.xscale("log")
plt.ylabel("Massenstreukoeffizient [cm²/g]")
plt.legend(loc="upper right", fontsize=8)
plt.title("Massenstreukoeffizient bei 20.2 keV")
#plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Pb_Massenabsorptionskoeffizient.png", dpi=600, bbox_inches='tight')
plt.show()
