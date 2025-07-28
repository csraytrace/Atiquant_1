from Nachbau_ati_sauber.Element import Element
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def Z_ber(a,b,x):
    return (x/a)**(1/b)
def power_law(x, a, b):
    return a * np.power(x, b)

coh = []
inc = []
x = list(range(1, 95))  # Ordnungszahlen 1 bis 100
Energie=20.2    #oder Emax? (oder Röhrenspek)
#Energie=20.2
#Energie=2.7
#Energie=40
for i in x:
    print(i)
    x_ele = Element(Element=str(i))
    #inc.append(x_ele.Tau_incoh_energie(Energie))  # inkohärent (Compton)
    #coh.append(x_ele.Tau_coh_energie(Energie))    # kohärent (Rayleigh)
    inc.append(x_ele.Tau_incoh_energie(19.3))  # inkohärent (Compton)
    coh.append(x_ele.Tau_coh_energie(20.2))    # kohärent (Rayleigh)


R=np.array(inc)/np.array(coh)

# Curve Fit durchführen
popt, pcov = curve_fit(power_law, x, R, p0=[200, -2])  # p0 = Startwerte für a, b

a_fit, b_fit = popt
print(f"Gefundene Parameter: a = {a_fit:.3f}, b = {b_fit:.3f}")

# Fit-Kurve berechnen
x_fit = np.linspace(min(x), max(x), 100)
y_fit = power_law(x_fit, a_fit, b_fit)

# Plotten
plt.scatter(x, R, label="Daten", color="red")
plt.plot(x_fit, y_fit, label=f"Fit: $y = {a_fit:.2f} \cdot x^{{{b_fit:.2f}}}$")

popt, pcov = curve_fit(power_law, x[1:30], R[1:30], p0=[200, -2])  # p0 = Startwerte für a, b

a_fit, b_fit = popt
print(f"Gefundene Parameter: a = {a_fit:.3f}, b = {b_fit:.3f}")

# Fit-Kurve berechnen
x_fit = np.linspace(min(x), max(x), 100)
y_fit = power_law(x_fit, a_fit, b_fit)

# Plotten
#plt.scatter(x, R, label="Daten", color="blue")
plt.plot(x_fit, y_fit, label=f"Fit: $y = {a_fit:.2f} \cdot x^{{{b_fit:.2f}}}$")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()







"""

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
"""
