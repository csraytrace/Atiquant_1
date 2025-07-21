import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

class PlotSwitcher:
    def __init__(self,  geo, save_path=None):
        self.datasets = []
        self.len = 0
        self.einstellung = 0

        self.index = 0
        self.geo = geo
        self.Dataset()

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        self.slider_ax = self.fig.add_axes([0.2, 0.1, 0.65, 0.03])
        self.slider = Slider(self.slider_ax, 'Bild', 0, len(self.datasets[1]) - 1, valinit=self.index, valstep=1)
        ##self.slider_ax.set_visible(False)
        #self.slider = Slider(self.slider_ax, '-Spannung' + str(-3 + self.index * 0.5), 0, len(self.datasets[1]) - 1, valinit=self.index, valstep=1)
        #self.slider = Slider(self.slider_ax, '+ Spannung', -3, 1, valinit=self.index, valstep=0.5)

        self.slider.on_changed(self.update_plot)


        self.plot_current()
        if (save_path is not None):
            plt.savefig(save_path, dpi=600, bbox_inches='tight')
            #plt.savefig(save_path)
        plt.show()

    def Dataset(self):
        geometriefaktor = []
        Energie = []
        for i in self.geo:
            zusatz = []
            for j in i:
                zusatz.append(j[0])
            geometriefaktor.append(np.array(zusatz))
        for i in self.geo[0]:
            Energie.append(i[1])
        self.datasets = (np.array(Energie), geometriefaktor)

        for i in range(len(self.geo[0])):
            if (i == 0):
                zeichen = self.geo[0][0][2]
            else:
                if (zeichen == self.geo[0][i][2]):
                    self.len = i
                    break
        return 0

    def plot_current(self):
        self.ax.clear()
        x, y = self.datasets[0], self.datasets[1][self.index]
        self.ax.plot(x[0:self.len], y[0:self.len], 'o',markersize=2, color="b", label=f"Geometriefaktoren 30keV")
        self.ax.plot(x[self.len*2:self.len*3], y[self.len*2:self.len*3], 'o',markersize=2, color="g", label=f"Geometriefaktoren 35keV")
        self.ax.plot(x[self.len:self.len*2], y[self.len:self.len*2], 'o',markersize=2, color="r", label=f"Geometriefaktoren 40keV") #{self.index + 1}

        self.ax.axhline(y=y.mean(), color='gray', linestyle='--', linewidth=0.5, label="Mittelwert Geo")
        self.ax.axhline(y=y.mean()*1.1, color='red', linestyle='--', linewidth=0.3, label="10% Intervall")
        self.ax.axhline(y=y.mean()*0.9, color='red', linestyle='--', linewidth=0.3)
        #self.ax.axhline(y=2.68e-5, color='green', linestyle='--', linewidth=0.3)
        #self.ax.set_ylim([y.mean() - 5e-5, y.mean()+5e-5])
        self.ax.set_ylim([3e-5 - 5e-5, 3e-5+5e-5])
        for i in range(self.len):
            #self.ax.annotate(self.geo[self.index][i][2], (self.geo[self.index][i][1], self.geo[self.index][i][0]*1.1), xytext=(0,10), textcoords="offset points")
            if (i % 2 == 0):
                self.ax.annotate(self.geo[self.index][i][2], (self.geo[self.index][i][1], self.geo[self.index][i][0]), xytext=(0,15), textcoords="offset points" ,
                                 arrowprops=dict(arrowstyle="-", linewidth=0.5, color="black" ))
            else:
                self.ax.annotate(self.geo[self.index][i][2], (self.geo[self.index][i][1], self.geo[self.index][i][0]), xytext=(0,35), textcoords="offset points" ,
                                 arrowprops=dict(arrowstyle="-", linewidth=0.5, color="grey" ))
            #print(y.mean()+5.0e-5)
        if (self.einstellung == 0):
            self.ax.set_title(f"Abweichung {Abweichung(y)*10**5:.3f}e-5" + "\nSpannungsänderung"+str(-3 + self.index * 0.5))
            self.ax.set_title(f"mittlere Abweichung {Abweichung(y)/y.mean()*100:.2f}%")
        else:
            self.ax.set_title(f"Abweichung {Abweichung(y)*10**5:.3f}e-5" + "\ncharzucont" + str(0.8 + self.index * 0.05))
        self.ax.set_xlabel('Energie [keV]')
        self.ax.set_ylabel('Geometriefaktor')

        self.ax.legend()
        self.fig.canvas.draw_idle()

    def update_plot(self, val):
        self.index = int(self.slider.val)
        self.plot_current()


def Abweichung(geo_list):
    mittelwert = geo_list.mean()
    abweichung = 0
    for i in geo_list:
        abweichung += abs(i - mittelwert)
    return abweichung / len(geo_list)



class Plot_einfach:
    def __init__(self, data, save_path=None, xy_format=True):
        """
        Konstruktor für die Klasse. Akzeptiert `data` entweder im xy-Format
        ([array[x], array[y], array[zeichen]]) oder als Liste von Listen ([[x1,y1,z1],...]).
        z muss nicht definiert sein.
        """
        self.datasets = []
        self.data = data
        self.save_path = save_path
        self.t2_format = xy_format
        self.Dataset()

    #def Abweichung(self,geo_list):
     #   mittelwert = geo_list.mean()
     #   abweichung = 0
      #  for i in geo_list:
      #      abweichung += abs(i - mittelwert)
       # return abweichung / len(geo_list)

    def Dataset(self):
        """
        Bereitet die Daten basierend auf dem xy- oder t1-Format auf.
        """
        if self.t2_format:
            # Verarbeitung für xy-Format
            Energie = np.array(self.data[0])
            y_data = np.array(self.data[1])
            Zeichen = self.data[2] if len(self.data) > 2 else [None] * len(Energie)
            x2 = np.array(self.data[-2]) if len(self.data) > 3 else np.full(len(self.data[0]), None)
            y2 = np.array(self.data[-1]) if len(self.data) > 3 else np.full(len(self.data[0]), None)
        else:
            # Verarbeitung für t1-Format
            y_data = np.array([i[1] for i in self.data])
            Energie = np.array([i[0] for i in self.data])
            Zeichen = [i[2] if len(i) > 2 else None for i in self.data]
            x2 = np.array([i[-2] if len(i) > 3 else None for i in self.data])
            y2 = np.array([i[-1] if len(i) > 3 else None for i in self.data])


        self.datasets = {
            "primary": (Energie, y_data, Zeichen),
            "secondary": (x2, y2),
        }
        return 0

    def plot_scatter(self, ax=None, **kwargs):
        """
        Erstellt einen Scatter-Plot mit Beschriftungen (falls vorhanden).
        """
        if not self.datasets:
            print("Keine Daten zum Plotten verfügbar.")
            return self

        # Extrahiere die Daten
        Energie, y_data, Zeichen = self.datasets["primary"]
        x2, y2 = self.datasets["secondary"]

        # Standard-Achse verwenden, falls keine angegeben ist
        if ax is None:
            ax = plt.gca()

        # Plot-Optionen aus kwargs
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", "label")  # Label
        color = kwargs.get("color", "blue")
        Abweichung = kwargs.get("abweichung", False)
        point_size = kwargs.get("point_size", 50)  # Punktgröße für Scatter
        #print(y_data)

        ymin = kwargs.get("ymin", min(y_data) * 0.9)  # Dynamisches oder fixes ymin
        ymax = kwargs.get("ymax", max(y_data) * 1.1)  # Dynamisches oder fixes ymax

        ax.set_ylim(ymin, ymax)

        # Scatter-Plot erstellen
        if (kwargs.get("label", "Secondary") != None):
            ax.scatter(Energie, y_data, c=color, s=point_size, label=Name)
        else:
            ax.scatter(Energie, y_data, c=color, s=point_size, label=Name)


        # Optional: Text hinzufügen
        if Zeichen and any(Zeichen):  # Prüfen, ob Zeichen vorhanden sind
            for i, (x, y, z) in enumerate(zip(Energie, y_data, Zeichen)):
                if z:  # Nur hinzufügen, wenn ein Zeichen existiert
                    va_position = 'bottom' if i % 2 == 0 else 'top'  # Abwechselnd oben und unten setzen
                    #va_position="top"
                    ax.text(x, y, z, fontsize=12, ha='right', va=va_position)

        if Abweichung:
            #print(y_data.mean())
            ax.axhline(y=y_data.mean(), color='gray', linestyle='--', linewidth=0.5, label="Mittelwert Geo")
            ax.axhline(y=y_data.mean()*1.1, color='red', linestyle='--', linewidth=0.3, label="10% Intervall")
            ax.axhline(y=y_data.mean()*0.9, color='red', linestyle='--', linewidth=0.3)
            #ax.set_title(f"mittlere Abweichung {self.Abweichung(y_data)/y_data.mean()*100:.2f}%")
            #ax.set_title(f"mittlere Abweichung {np.mean(np.abs(y_data - y_data.mean())) / y_data.mean()*100:.2f}%")
            ax.set_title(f"mittlere Abweichung {np.mean(np.abs(y_data - y_data.mean())) / y_data.mean()*100:.2f}%")

        else:
            ax.set_title(kwargs.get("title", "Scatter Plot mit zwei x-Achsen"))

        # Achsenskalierung
        if x_log:
            ax.set_xscale("log")
        if y_log:
            ax.set_yscale("log")

        # Achsenbeschriftung und Titel
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)


        if x2[0] is not None and y2[0] is not None:
            ax2 = ax.twinx()

            ymin2 = kwargs.get("ymin2", min(y2) * 0.9)  # Dynamisches oder fixes ymin
            ymax2 = kwargs.get("ymax2", max(y2) * 1.1)

            ax2.set_ylim(ymin2, ymax2)


            if (kwargs.get("label2", "Secondary") != None):
                ax2.scatter(x2, y2, c=kwargs.get("color2", "red"), label=kwargs.get("label2", "Secondary"))
            else:
                ax2.scatter(x2, y2, c=kwargs.get("color2", "red"))

            ax2.set_ylabel(kwargs.get("ylabel2", "y2"))

        # Titel und Legende

        ax.legend(loc="upper left")
        if x2[0] is not None and y2[0] is not None:
            ax2.legend(loc="upper right")


        return self

    def plot_line(self, ax=None, **kwargs):
        """
        Erstellt einen Line-Plot.
        """
        if not self.datasets:
            print("Keine Daten zum Plotten verfügbar.")
            return self


        # Extrahiere die Daten
        Energie, y_data, _ = self.datasets["primary"]
        x2, y2 = self.datasets["secondary"]

        # Standard-Achse verwenden, falls keine angegeben ist
        if ax is None:
            ax = plt.gca()

        # Plot-Optionen aus kwargs
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", None)  # Label
        color = kwargs.get("color", "blue")
        ymin = kwargs.get("ymin", min(y_data) * 0.9)  # Dynamisches oder fixes ymin
        ymax = kwargs.get("ymax", max(y_data) * 1.1)  # Dynamisches oder fixes ymax
        linestyle=kwargs.get("linestyle", '-')

        ax.set_ylim(ymin, ymax)

        # Line-Plot erstellen

        if (kwargs.get("label", "Secondary") != None):
            ax.plot(Energie, y_data, label=Name, color=color, linestyle=linestyle)
        else:
            ax.plot(Energie, y_data, color=color, linestyle=linestyle)


        # Achsenskalierung
        if x_log:
            ax.set_xscale("log")
        if y_log:
            ax.set_yscale("log")

        # Achsenbeschriftung
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if x2[0] is not None and y2[0] is not None:
            ax2 = ax.twinx()

            ymin2 = kwargs.get("ymin2", min(y2) * 0.9)  # Dynamisches oder fixes ymin
            ymax2 = kwargs.get("ymax2", max(y2) * 1.1)


            if kwargs.get("log_x2", False):
                ax2.set_xscale("log")
            if kwargs.get("log_y2", False):
                ax2.set_yscale("log")



            ax2.set_ylim(ymin2, ymax2)

            if (kwargs.get("label2", "Secondary") != None):
                ax2.plot(x2, y2, label=kwargs.get("label2", "Secondary"), color=kwargs.get("color2", "red"), linewidth=kwargs.get("linewidth2", 2))
                ax2.legend(loc="upper right")
            else:
                ax2.plot(x2, y2, color=kwargs.get("color2", "red"), linewidth=kwargs.get("linewidth2", 2))

            ax2.set_ylabel(kwargs.get("ylabel2", "y2"))

    # Titel und Legende
        ax.set_title(kwargs.get("title", "Line Plot mit zwei x-Achsen"))
        ax.legend(loc="upper left")

        return self




class Plot_einfach_alt:
    def __init__(self, data, save_path=None, xy_format=True):
        """
        Konstruktor für die Klasse. Akzeptiert `data` entweder im xy-Format
        ([array[x], array[y], array[zeichen]]) oder als Liste von Listen ([[x1,y1,z1],...]).
        z muss nicht definiert sein.
        """
        self.datasets = []
        self.data = data
        self.save_path = save_path
        self.t2_format = xy_format
        self.Dataset()

    #def Abweichung(self,geo_list):
     #   mittelwert = geo_list.mean()
     #   abweichung = 0
      #  for i in geo_list:
      #      abweichung += abs(i - mittelwert)
       # return abweichung / len(geo_list)

    def Dataset(self):
        """
        Bereitet die Daten basierend auf dem xy- oder t1-Format auf.
        """
        if self.t2_format:
            # Verarbeitung für xy-Format
            Energie = np.array(self.data[0])
            y_data = np.array(self.data[1])
            Zeichen = self.data[2] if len(self.data) > 2 else [None] * len(Energie)
        else:
            # Verarbeitung für t1-Format
            y_data = [i[1] for i in self.data]
            Energie = [i[0] for i in self.data]
            Zeichen = [i[2] if len(i) > 2 else None for i in self.data]

        self.datasets = (np.array(Energie), np.array(y_data), Zeichen)
        return 0

    def plot_scatter(self, ax=None, **kwargs):
        """
        Erstellt einen Scatter-Plot mit Beschriftungen (falls vorhanden).
        """
        if not self.datasets:
            print("Keine Daten zum Plotten verfügbar.")
            return self

        # Extrahiere die Daten
        Energie, y_data, Zeichen = self.datasets

        # Standard-Achse verwenden, falls keine angegeben ist
        if ax is None:
            ax = plt.gca()

        # Plot-Optionen aus kwargs
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", "label")  # Label
        color = kwargs.get("color", "blue")
        Abweichung = kwargs.get("abweichung", False)
        point_size = kwargs.get("point_size", 50)  # Punktgröße für Scatter

        ymin = kwargs.get("ymin", min(y_data) * 0.9)  # Dynamisches oder fixes ymin
        ymax = kwargs.get("ymax", max(y_data) * 1.1)  # Dynamisches oder fixes ymax

        ax.set_ylim(ymin, ymax)

        # Scatter-Plot erstellen
        ax.scatter(Energie, y_data, c=color, s=point_size, label=Name)

        # Optional: Text hinzufügen
        if Zeichen and any(Zeichen):  # Prüfen, ob Zeichen vorhanden sind
            for x, y, z in zip(Energie, y_data, Zeichen):
                if z:  # Nur hinzufügen, wenn ein Zeichen existiert
                    ax.text(x, y, z, fontsize=12, ha='right', va='bottom')


        if Abweichung:
            #print(y_data.mean())
            ax.axhline(y=y_data.mean(), color='gray', linestyle='--', linewidth=0.5, label="Mittelwert Geo")
            ax.axhline(y=y_data.mean()*1.1, color='red', linestyle='--', linewidth=0.3, label="10% Intervall")
            ax.axhline(y=y_data.mean()*0.9, color='red', linestyle='--', linewidth=0.3)
            #ax.set_title(f"mittlere Abweichung {self.Abweichung(y_data)/y_data.mean()*100:.2f}%")
            ax.set_title(f"mittlere Abweichung {np.mean(np.abs(y_data - y_data.mean())) / y_data.mean()*100:.2f}%")

        # Achsenskalierung
        if x_log:
            ax.set_xscale("log")
        if y_log:
            ax.set_yscale("log")

        # Achsenbeschriftung und Titel
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)


        return self

    def plot_line(self, ax=None, **kwargs):
        """
        Erstellt einen Line-Plot.
        """
        if not self.datasets:
            print("Keine Daten zum Plotten verfügbar.")
            return self

        # Extrahiere die Daten
        Energie, y_data, _ = self.datasets

        # Standard-Achse verwenden, falls keine angegeben ist
        if ax is None:
            ax = plt.gca()

        # Plot-Optionen aus kwargs
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", "label")  # Label
        color = kwargs.get("color", "blue")
        ymin = kwargs.get("ymin", min(y_data) * 0.9)  # Dynamisches oder fixes ymin
        ymax = kwargs.get("ymax", max(y_data) * 1.1)  # Dynamisches oder fixes ymax
        linewidth = kwargs.get("linewidth", 2)  # Linienbreite

        ax.set_ylim(ymin, ymax)

        # Line-Plot erstellen
        ax.plot(Energie, y_data, label=Name, color=color, linewidth=linewidth)

        # Achsenskalierung
        if x_log:
            ax.set_xscale("log")
        if y_log:
            ax.set_yscale("log")

        # Achsenbeschriftung
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return self

    def plot_line(self, ax=None, **kwargs):
        """
        Erstellt einen Line-Plot.
        """
        if not self.datasets:
            print("Keine Daten zum Plotten verfügbar.")
            return self

        # Extrahiere die Daten
        Energie, y_data, _ = self.datasets

        # Standard-Achse verwenden, falls keine angegeben ist
        if ax is None:
            ax = plt.gca()

        # Plot-Optionen aus kwargs
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", "label")  # Label
        color = kwargs.get("color", "blue")
        linewidth = kwargs.get("linewidth", 2)  # Linienbreite

        # Line-Plot erstellen
        ax.plot(Energie, y_data, label=Name, color=color, linewidth=linewidth)

        # Logarithmische Skalierung
        if x_log:
            ax.set_xscale("log")
        if y_log:
            ax.set_yscale("log")

        # Achsenbeschriftung
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return self

class InteractivePlot:
    def __init__(self, plot_data_list, settings_list=None, scatter=False, **kwargs):
        """
        Initialisiert die interaktive Plot-Klasse.

        :param plot_data_list: Liste von `Plot_einfach`-Objekten
        :param settings_list: Liste der Einstellungen für jeden Plot
        :param scatter: Ob Scatter-Plots oder Line-Plots verwendet werden sollen
        :param kwargs: Zusätzliche Argumente für die Plotmethoden
        """
        self.scatter = scatter
        self.plot_data_list = plot_data_list
        self.settings_list = settings_list  # Einstellungen speichern
        self.current_index = 0
        self.plot_kwargs = kwargs  # Zusätzliche Plot-Optionen

        # Erstellen des Hauptplots
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(bottom=0.2)  # Platz für den Slider schaffen

        # Hinzufügen eines Sliders
        self.slider_ax = plt.axes([0.2, 0.05, 0.6, 0.03])  # Position des Sliders
        self.slider = Slider(
            ax=self.slider_ax,
            label='Plot Index',
            valmin=0,
            valmax=len(plot_data_list) - 1,
            valinit=self.current_index,
            valstep=1
        )

        # Event für den Slider registrieren
        self.slider.on_changed(self.update_plot)

        # Erster Plot anzeigen
        self.update_plot(self.current_index)

    def update_plot(self, index):
        """
        Aktualisiert den Plot basierend auf dem Sliderwert.
        """
        self.current_index = int(index)
        self.ax.clear()  # Vorherigen Plot löschen

        # Aktuellen Plot zeichnen
        plot_obj = self.plot_data_list[self.current_index]
        current_setting = (
            self.settings_list[self.current_index]
            if self.settings_list is not None
            else "Keine Einstellung"
        )

        # Den Scatterplot oder Line-Plot zeichnen
        if self.scatter:
            plot_obj.plot_scatter(ax=self.ax, **self.plot_kwargs)
        else:
            plot_obj.plot_line(ax=self.ax, **self.plot_kwargs)

        # Einstellung[i] als Text im Plot anzeigen
        self.ax.text(
            0.05, 0.95,  # Position relativ zum Plot (x, y in Prozent des Achsenbereichs)
            f"Einstellung: {current_setting}",
            transform=self.ax.transAxes,
            fontsize=10,
            color="gray",
            ha="left",
            va="top",
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="white")
        )

        # Neu zeichnen
        self.ax.legend()
        self.fig.canvas.draw_idle()

    def show(self):
        """
        Zeigt das interaktive Plot-Fenster an.
        """
        plt.show()

#data1 = [[1, 2, 3], [4, 5, 6], ['A', 'B', 'C']]
#data2 = [[2, 3, 4], [6, 7, 8], ['X', 'Y', 'Z']]
#data3 = [[3, 4, 5], [8, 9, 10], ['P', 'Q', 'R']]

#plot1 = Plot_einfach(data1)
#plot2 = Plot_einfach(data2)
#plot3 = Plot_einfach(data3)

#interactive_plot = InteractivePlot([plot1, plot2, plot3],scatter=False)
#interactive_plot.show()

#x1 = np.array([1, 2, 3])
#y1 = np.array([3, 4, 5])
#x2 = np.array([1, 2, 3])
#y2 = np.array([6, 7, 8])
#x3 = np.array([1, 2, 3])
#y3 = np.array([9, 10, 1144])

#datasets = [(x1, y1), (x2, y2), (x3, y3)]

#plot_switcher = PlotSwitcher(datasets)
   # def update_plot(self, index):
    #    """
    ##    Aktualisiert den Plot basierend auf dem Sliderwert.
#
    #    :param index: Aktueller Index des Sliders
    #    """
     #   self.current_index = int(index)
    #    self.ax.clear()  # Vorherigen Plot löschen

        # Aktuellen Plot zeichnen
    #    plot_obj = self.plot_data_list[self.current_index]

   #     # Beispiel: Beide Plots anzeigen
   #     if self.scatter:
    #        plot_obj.plot_scatter(ax=self.ax, label=f"Scatter {self.current_index}")
    #    else:
    #        plot_obj.plot_line(ax=self.ax, label=f"Line {self.current_index}")

     #   # Neu zeichnen
    #    self.ax.legend()
   #     self.fig.canvas.draw_idle()
