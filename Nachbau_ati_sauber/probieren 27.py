import numpy as np
from scipy.optimize import curve_fit

# Daten
Energie_array = [3.56, 3.7273, 3.7571, 3.9904, 4, 4.0224, 5, 6, 8, 10, 15, 20, 26.663, 26.876, 30, 40, 50]
Werte_Sco = [146140, 130660, 128110, 110760, 110100, 108570, 59859, 35742, 15451, 7891, 2225, 878, 338.5, 329.6, 227.6, 85.3, 39.4]

# Konvertiere Liste in numpy-Array
Energie_array = np.array(Energie_array)

# Potenzfunktion y = a * x^b
def power_law(x, a, b):
    return a * np.power(x, b)

# Exponentielle Funktion y = a * exp(b * x)
def exponential_func(x, a, b):
    return a * np.exp(b * x)

# Quadratisches Polynom y = a * x^2 + b * x + c
def polynomial_func(x, a, b, c):
    return a * np.power(x, 2) + b * x + c

# Curve Fit für alle Modelle
popt_power, _ = curve_fit(power_law, Energie_array, Werte_Sco)
popt_exp, _ = curve_fit(exponential_func, Energie_array, Werte_Sco)
popt_poly, _ = curve_fit(polynomial_func, Energie_array, Werte_Sco)

# Berechnung der Residuen
residuals_power = np.array(Werte_Sco) - power_law(Energie_array, *popt_power)
residuals_exp = np.array(Werte_Sco) - exponential_func(Energie_array, *popt_exp)
residuals_poly = np.array(Werte_Sco) - polynomial_func(Energie_array, *popt_poly)

# Summe der quadrierten Residuen (SSR)
ssr_power = np.sum(residuals_power**2)
ssr_exp = np.sum(residuals_exp**2)
ssr_poly = np.sum(residuals_poly**2)

# Ausgabe der Fehler für die Modelle
print(f"Potenzfunktion SSR: {ssr_power}")
print(f"Exponentielle Funktion SSR: {ssr_exp}")
print(f"Quadratisches Polynom SSR: {ssr_poly}")
