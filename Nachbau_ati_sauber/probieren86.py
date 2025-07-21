import re
import numpy as np

file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\Fit_pymca\\SOIL7.spe_1.1.1.1.fit'
file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\pymca_dat\\AL.spe_1.1.1.1.fit'

#with open(file_path, "r", encoding="utf-8") as file:
 #   for line in file:
 #       if re.match(r"^y", line):  # ^y bedeutet "Zeile beginnt mit y"

def read_arrays_from_file(filename):
    arrays = {}  # Dictionary für gefundene Arrays
    current_key = None  # Name des aktuellen Arrays
    collecting = False  # Flag, um das Sammeln von Werten zu steuern
    array_values = []  # Temporäre Liste für Zahlen

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            # Falls die Zeile mit "y" gefolgt von einem Buchstaben beginnt (z. B. "yRh Kb =")
            match = re.match(r"^(y[A-Za-z]+\s+[A-Za-z]+)\s*=", line)
            if match:
                # Falls vorher schon ein Array gesammelt wurde, speichere es ab
                if current_key and array_values:
                    arrays[current_key] = np.array(array_values)

                # Starte das Sammeln eines neuen Arrays
                current_key = match.group(1)  # Array-Name (z. B. "yRh Kb")
                array_values = []
                collecting = True

            # Falls wir innerhalb eines Arrays sind, alle Zahlen sammeln
            if collecting:
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)  # Alle Zahlen extrahieren
                if numbers:
                    array_values.extend(map(float, numbers))

                # Falls die Zeile eine `]` enthält, beende das Sammeln
                if "]" in line:
                    collecting = False
                    arrays[current_key] = np.array(array_values)

    return arrays  # Alle gefundenen Arrays zurückgeben

print(read_arrays_from_file(file_path))
arrays = (read_arrays_from_file(file_path))
for key, array in arrays.items():
    print(f"\nArray '{key}':")
    print(array)
    print(array.sum())
    print(f"Anzahl der Werte: {len(array)}")
