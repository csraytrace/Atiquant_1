import numpy as np
import matplotlib.pyplot as plt
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

    def plot(self, x_data, y_data, z_data, plot_type='scatter', interpolation_method='linear', line_coords=None, extra_points=None, log_scale=False):
        """
        Erstellt einen 3D-Plot basierend auf den übergebenen Daten.
        :param x_data: Daten für die X-Achse
        :param y_data: Daten für die Y-Achse
        :param z_data: Daten für die Z-Achse
        :param plot_type: Art des Plots ('scatter', 'line', 'surface')
        :param interpolation_method: Interpolationsmethode für Surface Plot ('linear', 'cubic', 'nearest')
        :param line_coords: Koordinaten für die Gerade (x_line, y_line, z_line)
        :param extra_points: Zusätzliche Punkte (x_extra, y_extra, z_extra) für Punkte, die durch eine Linie verbunden sind
        :param log_scale: Wenn True, z-Werte logarithmisch plotten
        """
        # Falls log_scale aktiviert ist, wende logarithmische Transformation auf z_data an
        if log_scale:
            pass
            z_data = np.log(z_data)
            if line_coords:
                line_coords = (line_coords[0], line_coords[1], np.log(line_coords[2]))
            if extra_points:
                extra_points = (extra_points[0], extra_points[1], np.log(extra_points[2]))

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
            ax.scatter(x_data, y_data, z_data, c='r', marker='o', label='Chi Square Punkte')

        # Falls Koordinaten für eine Gerade übergeben werden, plotte die Gerade
        if line_coords:
            x_line, y_line, z_line = line_coords
            ax.plot(x_line, y_line, z_line, color='blue', linewidth=2, label='Minimum Gerade')

        # Falls zusätzliche Punkte angegeben sind, die durch eine Linie verbunden werden sollen
        if extra_points:
            x_extra, y_extra, z_extra = extra_points
            ax.scatter(x_extra, y_extra, z_extra, color='black',s=60, marker='o', label='NLLS-Werte')
            ax.plot(x_extra, y_extra, z_extra, color='black',linewidth=2.5, linestyle='--', label='NLLS-Schritte')

        # Beschriftung der Achsen und Titel
        ax.set_title(self.title)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        if (log_scale == True):
            ax.set_zlabel(self.zlabel + " (log)")
            #ax.set_zscale('log')
        else:
            ax.set_zlabel(self.zlabel)


        plt.legend()
        plt.show()

# Beispiel zur Nutzung der Klasse
if __name__ == "__main__":
    # Beispielhafte Daten
    x_data = np.tile(np.linspace(0, 1, 10), 10)
    y_data = np.repeat(np.linspace(0, 1, 10), 10)
    z_data = np.sin(np.pi * x_data) * np.cos(np.pi * y_data) + 1.1  # Beispielhafte Z-Daten (verschoben, um positive Werte zu garantieren)

    # Geradenkoordinaten (z.B. eine Gerade von (0, 0, 0) bis (1, 1, 1))
    x_line = np.linspace(0, 1, 10)
    y_line = np.linspace(0, 1, 10)
    z_line = np.linspace(1, 10, 10)  # Logarithmische Werte müssen positiv sein

    # Zusätzliche Punkte für Scatterplot, verbunden durch eine Linie
    x_extra = np.linspace(0.5, 1, 5)
    y_extra = np.linspace(0.5, 1, 5)
    z_extra = np.linspace(1, 10, 5)  # Positive Werte für log

    # Instanziere die Klasse
    plotter = DreidimensionalerPlot(title="3D Plot mit logarithmischen Z-Werten", xlabel="X-Achse", ylabel="Y-Achse", zlabel="Z-Achse")

    # Streuplot mit einer Gerade (logarithmische Z-Werte)
    plotter.plot(x_data, y_data, z_data, plot_type='scatter', line_coords=(x_line, y_line, z_line), log_scale=True)

    # Oberflächenplot mit einer zusätzlichen Linie und Punkten (logarithmische Z-Werte)
    plotter.plot(x_data, y_data, z_data, plot_type='surface', interpolation_method='linear', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra), log_scale=True)
