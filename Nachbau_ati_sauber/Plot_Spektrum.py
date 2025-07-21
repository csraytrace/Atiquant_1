import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Klasse Plotter
class Plotter:
    def __init__(self, data):
        """
        :param data: Ein Array von Arrays mit (x, y)-Tupeln.
        """
        self.data = data

    def show_plot_with_slider(self):
        # Initialisierung des Plots
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        # Ersten Datensatz plotten
        x, y = self.data[0]
        line, = ax.plot(x, y, label="Plot 0")
        ax.set_xlabel("X-Werte")
        ax.set_ylabel("Y-Werte")
        ax.set_title("Wechselbare Plots")
        ax.legend()

        # Slider hinzufügen
        ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor="lightgoldenrodyellow")
        slider = Slider(ax_slider, "Plot Index", 0, len(self.data) - 1, valinit=0, valstep=1)

        # Update-Funktion für den Slider
        def update(val):
            idx = int(slider.val)
            x, y = self.data[idx]
            line.set_xdata(x)  # X-Daten aktualisieren
            line.set_ydata(y)  # Y-Daten aktualisieren
            line.set_label(f"Plot {idx}")  # Legende aktualisieren
            ax.legend()
            fig.canvas.draw_idle()  # Plot aktualisieren

        slider.on_changed(update)  # Slider mit Update-Funktion verbinden

        plt.show()

# Beispiel-Daten erstellen
def create_example_data():
    data = []
    for i in range(10):  # 10 verschiedene Plots
        x = np.linspace(0, 10, 100)
        y = np.sin(x + i)  # Verschiedene Sinus-Kurven
        data.append((x, y))
    return data

# Nutzung der Klassen
example_data = create_example_data()
plotter = Plotter(example_data)
plotter.show_plot_with_slider()
