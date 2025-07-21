from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#x1, x2 = 3.54, 35
x1, x2 = 3.54, 8


Emax = 40
Ele = "cd"
step = 0.01

x_Ele = Element(Element = Ele, Emax = Emax, step = step)

Tube = Röhre(Emax = Emax, step = step)


#Emax neu

x_Ele = Element(Element = Ele, Emax = Emax, step = step)
#Tube = Röhre(Emax = Emax, step = step)

for index, i in enumerate(Tube.Countrate_gesamt[0]):
    if (x_Ele.Kanten()[3][1] < i):
        break

#für L3
Sij_L3 = []
for Energie in Tube.Countrate_gesamt[0]:
    Sij_L3.append(x_Ele.S_ij("L3", Energie))

Sij_L3 = np.array(Sij_L3)

#für Pb
Energie_array = [13.13, 15, 15.236, 15.358, 15.841, 15.968, 20, 30, 40, 50, 60]
Werte_Sco = [32049, 22203, 21298, 20853, 19212, 18808, 9961, 3007, 1251, 624, 351]

#für Cd
Energie_array = [3.56, 3.7273, 3.7571, 3.9904, 4, 4.0224, 5, 6, 8, 10, 15, 20, 26.663, 26.876, 30, 40, 50]
Werte_Sco = [146140, 130660, 128110, 110760, 110100, 108570, 59859, 35742, 15451, 7891, 2225, 878, 338.5, 329.6, 227.6, 85.3, 39.4]

Werte_Sco = np.array(Werte_Sco)
Werte_Sco =  Werte_Sco * x_Ele.Get_cm2g()

def fit_func(x, a, b):
    return a * np.power(x, b)

#def fit_func(x, a, b):
 #   return a * np.exp(b * x)


# Curve Fit durchführen
popt, pcov = curve_fit(fit_func, Energie_array, Werte_Sco)

# Die gefitteten Parameter a und b
a, b = popt
print(f"Gefittete Parameter: a = {a}, b = {b}")

# Fit-Kurve berechnen
Energie_fit = np.linspace(min(Energie_array), max(Energie_array), 100)
Werte_fit = fit_func(Energie_fit, a, b)

# Plot der Daten und des Fits
plt.scatter(Energie_array, Werte_Sco, label='Daten', c='red')
plt.plot(Energie_fit, Werte_fit, label=f'Fit: y = {a:.2f} * x^{b:.2f}', color='green')

plt.xlabel('Energie')
plt.ylabel('Werte Sco')


#plt.plot(Tube.Countrate_gesamt[0][index:], Tube.Countrate_gesamt[1][index:] * Sij_L3[index:] * x_Ele.tau[1][index:])
plt.plot(Tube.Countrate_gesamt[0][index:], Sij_L3[index:] * x_Ele.tau[1][index:], label= "Atiquant")
#plt.scatter(Energie_array, Werte_Sco )

tau_sco = [fit_func(Energie, a, b) for Energie in x_Ele.tau[0][index:]]
tau_sco = np.array(tau_sco)

Summe = (Tube.Countrate_gesamt[1][index:] * Sij_L3[index:] * x_Ele.tau[1][index:]).sum()

Summe2 = (Tube.Countrate_gesamt[1][index:]  * tau_sco).sum()

print(Summe)
print(Summe2)
print(Summe/Summe2)
#plt.plot(x_Ele.tau[0][index:], tau_sco, label=f'Fit: y = {a:.2f} * x^{b:.2f}', color='red')

#plt.axvline(x=x1, color='r', linestyle='--', label='x1')
#plt.axvline(x=x2, color='b', linestyle='--', label='x2')





plt.title("Element: "+x_Ele.Get_Elementsymbol() + "   Abweichung  "+ str(f"{Summe/Summe2 *100:.3f}"))
#plt.xscale('log')
#plt.yscale('log')

plt.legend()
#plt.grid(True)

plt.show()

