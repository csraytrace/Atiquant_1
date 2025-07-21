import numpy as np

# Beispielarray
arr = np.array([0.5, 1.0, 2.0, 0.8, 1.2])

# Für alle Werte < 1 wird der Kehrwert berechnet, ansonsten bleibt der Wert gleich
result = np.where(arr < 1, 1 / arr, arr)

print("Original:", arr)
print("Transformiert:", result)
