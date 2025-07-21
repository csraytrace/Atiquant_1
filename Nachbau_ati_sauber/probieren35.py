import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

class DreidimensionalerPlot:
    def __init__(self, title="3D Plot", xlabel="X-Achse", ylabel="Y-Achse", zlabel="Z-Achse"):
        """
        Initialisiert die Klasse für den 3D-Plot.
        :param title: Titel des Plots
        :param xlabel: Beschriftung der X-Achse
        :param ylabel: Beschriftung der Y-Achse
        :param zlabel: Beschriftung der Z-Achse
        """
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel

    def plot(self, x_data, y_data, z_data, plot_type='scatter', interpolation_method='linear'):
        """
        Erstellt einen 3D-Plot basierend auf den übergebenen Daten.
        :param x_data: Daten für die X-Achse
        :param y_data: Daten für die Y-Achse
        :param z_data: Daten für die Z-Achse
        :param plot_type: Art des Plots ('scatter', 'line', 'surface')
        :param interpolation_method: Interpolationsmethode für Surface Plot ('linear', 'cubic', 'nearest')
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot-Typen: Streudiagramm, Liniendiagramm, oder Oberflächenplot
        if plot_type == 'scatter':
            ax.scatter(x_data, y_data, z_data, c='r', marker='o', label='Scatter Points')
        elif plot_type == 'line':
            ax.plot(x_data, y_data, z_data, color='blue')
        elif plot_type == 'surface':
            # Erstelle ein Gitter für die X- und Y-Daten
            grid_x, grid_y = np.meshgrid(np.linspace(min(x_data), max(x_data), 100),
                                         np.linspace(min(y_data), max(y_data), 100))

            # Interpoliere die Scatterdaten auf das Gitter
            grid_z = griddata((x_data, y_data), z_data, (grid_x, grid_y), method=interpolation_method)

            # Prüfe, ob NaN-Werte vorhanden sind, und fülle sie auf
            if np.isnan(grid_z).any():
                grid_z = np.nan_to_num(grid_z)  # NaN-Werte mit 0 auffüllen (oder wähle eine andere Strategie)

            # Zeichne den Surface Plot
            ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', alpha=0.6)

            # Zeichne auch die Scatterpunkte zur Veranschaulichung
            ax.scatter(x_data, y_data, z_data, c='r', marker='o', label='Scatter Points')

        # Beschriftung der Achsen und Titel
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_zlabel(self.zlabel)

        plt.show()

# Beispiel zur Nutzung der Klasse
if __name__ == "__main__":
    # Beispielhafte Daten
    x_data = np.tile(np.linspace(0, 1, 10), 10)
    y_data = np.repeat(np.linspace(0, 1, 10), 10)
    z_data = np.sin(np.pi * x_data) * np.cos(np.pi * y_data)  # Beispielhafte Z-Daten

    # Instanziere die Klasse
    plotter = DreidimensionalerPlot(title="3D Scatter and Surface Plot", xlabel="X-Achse", ylabel="Y-Achse", zlabel="Z-Achse")

    # Streuplot
    plotter.plot(x_data, y_data, z_data, plot_type='scatter')

    # Oberflächenplot basierend auf Scatterpunkten, mit linearer Interpolation
    plotter.plot(x_data, y_data, z_data, plot_type='surface', interpolation_method='linear')
