import tkinter as tk
from tkinter import messagebox

# Funktion zur Berechnung der Summe
def berechne_summe():
    try:
        wert1 = float(entry1.get())
        wert2 = float(entry2.get())
        summe = wert1 + wert2
        label_ergebnis.config(text=f"Ergebnis: {summe}")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Summenberechnung")
root.geometry("300x200")

# Label und Eingabefeld für den ersten Wert
label1 = tk.Label(root, text="Wert 1:")
label1.pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack(pady=5)

# Label und Eingabefeld für den zweiten Wert
label2 = tk.Label(root, text="Wert 2:")
label2.pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack(pady=5)

# Button zur Berechnung
button = tk.Button(root, text="Berechne Summe", command=berechne_summe)
button.pack(pady=10)

# Label zur Anzeige des Ergebnisses
label_ergebnis = tk.Label(root, text="Ergebnis: ")
label_ergebnis.pack(pady=10)

# Ereignisschleife starten
root.mainloop()
