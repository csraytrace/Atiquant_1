import numpy as np
from scipy.optimize import least_squares


x = np.array([0, 1, 2, 3, 4])
y = np.array([2, 5.4, 14.8, 40.2, 109.2])

# Residuenfunktion: modell - messung
def residuals(params, x, y):
    a, b = params
    y_model = a * np.exp(b * x)
    #print("f(x)?",y_model - y)
    return y_model - y


initial_guess = [0.1, 14]
initial_guess = [2, 2]

# Fit durchführen
result = least_squares(residuals, initial_guess, args=(x, y), max_nfev=1000, method="trf")

# Ergebnis
a_fit, b_fit = result.x
print("Gefittete Parameter: a =", a_fit, "b =", b_fit)
print("Sollte etwa a ~ 2, b ~ 0.9 (oder ähnlich) ergeben.")

# Optional: Modellwerte für Vergleich ausgeben
print("Gefittete y-Werte:", a_fit * np.exp(b_fit * x))
print("Original y-Werte:", y)


print(residuals([-1.69014261e-10 , 1.40000002e+01],x,y))
