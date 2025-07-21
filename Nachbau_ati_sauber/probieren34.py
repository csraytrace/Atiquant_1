from Nachbau_ati_sauber.probieren32 import DreidimensionalerPlot
import numpy as np


Geo = 4 * 10**-7 * 61 * 1.0066


x_data = np.tile(np.linspace(0, 1, 10), 10)
y_data = np.repeat(np.linspace(0, 1, 10), 10)

non_zero_indices = (x_data != 0) & (y_data != 0)  # Nur die Werte behalten, die in x und y nicht Null sind
x_data_filtered = x_data[non_zero_indices]
y_data_filtered = y_data[non_zero_indices]

print(x_data_filtered)
print(y_data_filtered)
