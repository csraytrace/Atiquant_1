import tkinter as tk
from tkinter import messagebox
import numpy as np

def berechne_verteilung():
    try:
        # Eingabe aus dem Textfeld auslesen und in eine Liste umwandeln
        eingabe_text = eingabe_feld.get()
        werte = list(map(float, eingabe_text.split(",")))  # Erwartet Zahlen durch Komma getrennt

        # Normiere die Werte (Summe auf 1 setzen)
        werte_summe = sum(werte)
        if werte_summe == 0:
            raise ValueError("Die Summe der Werte darf nicht 0 sein.")

        normierte_werte = [w / werte_summe for w in werte]

        # Ergebnis im Label anzeigen
        ergebnis_label.config(text="Normierte Werte: " + ", ".join(f"{w:.3f}" for w in normierte_werte))

    except ValueError as e:
        messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Verteilungsrechner")

# Eingabefeld
tk.Label(root, text="Gib die Verteilung ein (z. B. 10,20,30):").pack()
eingabe_feld = tk.Entry(root, width=40)
eingabe_feld.pack()

# Berechnungs-Button
berechnen_button = tk.Button(root, text="Berechnen", command=berechne_verteilung)
berechnen_button.pack()

# Ergebnis-Anzeige
ergebnis_label = tk.Label(root, text="Normierte Werte erscheinen hier", fg="blue")
ergebnis_label.pack()

# Tkinter-Hauptloop starten
root.mainloop()
