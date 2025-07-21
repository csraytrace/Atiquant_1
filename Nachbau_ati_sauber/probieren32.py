import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

    def plot(self, x_data, y_data, z_data, plot_type='scatter'):
        """
        Erstellt einen 3D-Plot basierend auf den übergebenen Daten.
        :param x_data: Daten für die X-Achse
        :param y_data: Daten für die Y-Achse
        :param z_data: Daten für die Z-Achse
        :param plot_type: Art des Plots ('scatter', 'line', 'surface')
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot-Typen: Streudiagramm, Liniendiagramm, oder Oberflächenplot
        if plot_type == 'scatter':
            ax.scatter(x_data, y_data, z_data, c='r', marker='o')
        elif plot_type == 'line':
            ax.plot(x_data, y_data, z_data, color='blue')
        elif plot_type == 'surface':
            X, Y = np.meshgrid(x_data, y_data)
            Z = np.sin(np.sqrt(X**2 + Y**2))  # Beispieloberfläche
            ax.plot_surface(X, Y, Z, cmap='viridis')

        # Beschriftung der Achsen und Titel
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_zlabel(self.zlabel)

        plt.show()

# Beispiel zur Nutzung der Klasse
if __name__ == "__main__":
    # Beispielhafte Daten
    x_data = np.linspace(-5, 5, 100)
    y_data = np.linspace(-5, 5, 100)
    z_data = np.sin(np.sqrt(x_data**2 + y_data**2))

    # Instanziere die Klasse
    plotter = DreidimensionalerPlot(title="Mein 3D-Plot", xlabel="X-Achse", ylabel="Y-Achse", zlabel="Z-Achse")

    # Streuplot
    plotter.plot(x_data, y_data, z_data, plot_type='scatter')

    # Linienplot
    plotter.plot(x_data, y_data, z_data, plot_type='line')

    # Oberflächenplot
    plotter.plot(x_data, y_data, z_data, plot_type='surface')
