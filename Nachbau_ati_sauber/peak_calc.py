import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.probieren99_fürtrac import *
Channel = 0.02

class Intensity():
    def __init__(self, spec, min_y=100, peak=None, interval=None, titel=None, abfallend=False):
        self.y, self.x = np.array(spec[0]), np.array(spec[1])
        self.titel = titel
        self.min_y = min_y
        self.abfallend=abfallend
        # Wenn ein Intervall angegeben wurde, direkt verwenden:
        if interval is not None:
            # Umrechnung der Energie in den entsprechenden Index:
            self.anfang = int(interval[0] / Channel)
            self.ende = int(interval[1] / Channel)
            # Falls du dennoch ein feines Anpassen wünschst, kannst du hier später check/Bereich aufrufen.
        elif peak is not None:
            self.anfang = int(peak / Channel)
            self.ende = int(peak / Channel)
            self.check()
            self.Bereich()
        else:
            self.anfang = None
            self.ende = None
            self.check()
            self.Bereich()
        self.Spekt = []
        self.Backround = []
        self.Balken()

    def check(self):
        if self.anfang is None:
            self.anfang = np.argmax(self.y)
            self.ende = np.argmax(self.y)

    def Bereich(self):
        flag = True
        while flag:
            if self.anfang == 0:
                flag = False
            elif self.y[self.anfang - 1] <= self.y[self.anfang] or self.y[self.anfang] > self.min_y:
                self.anfang -= 1
            else:
                flag = False
        flag = True
        while flag:
            if self.ende >= len(self.y) - 1:
                flag = False
            elif self.y[self.ende] >= self.y[self.ende + 1] or self.y[self.ende] > self.min_y:
                self.ende += 1
            else:
                flag = False

    def Balken(self):
        # Berechnet einen linearen Hintergrund im Peak-Bereich
        k = (self.y[self.ende] - self.y[self.anfang]) / (self.ende - self.anfang + 1)
        # Korrektur, falls das Verhältnis kleiner als 1 ist:
        if self.y[self.ende] / self.y[self.anfang] < 1:
            k = (self.y[self.anfang] - self.y[self.ende]) / (self.ende - self.anfang + 1) * (-1)
        gesamtzahl = []
        abzug = []
        for i in range(self.ende - self.anfang + 1):
            gesamtzahl.append(self.y[self.anfang + i])
            abzug.append(int(self.y[self.anfang] + k * i))
        self.Spekt = np.array(gesamtzahl)
        self.Backround = np.array(abzug)
        if self.abfallend:
            self.Spekt=enforce_monotonicity_from_peak(self.Spekt)

    def Plot(self, ax=None):
        created_fig = False
        if ax is None:
            fig, ax = plt.subplots()
            created_fig = True
        # Beschriftung mit Netto-Fläche:
        label = "Netarea: " + str(self.Spekt.sum()) + "-" + str(self.Backround.sum())
        # Gesamtspektrum plotten
        ax.plot(self.x, self.y, color="g", label=label)
        # Bereichsgrenzen markieren
        ax.axvline(x=self.anfang * Channel, color='r', linestyle='--', label='Anfang')
        ax.axvline(x=self.ende * Channel, color='r', linestyle='--', label='Ende')
        # Balken für Signal und Hintergrund zeichnen
        ax.bar(self.x[self.anfang:self.ende+1], self.Spekt, width=Channel, align='center')
        ##ax.bar(self.x[self.anfang:self.ende+1], self.Backround, width=Channel, align='center', color="r")
        if self.titel is not None:
            ax.set_title(self.titel)
        ax.set_xlabel("E [keV]")
        ax.set_ylabel("Counts")
        # Bestimme das Maximum im betrachteten Bereich und speichere es als Attribut
        region = self.y[self.anfang:self.ende+1]
        region_max = np.max(region)
        self.region_max = region_max
        max_index = np.argmax(region) + self.anfang
        ax.annotate(f"Max: {region_max}",
                    xy=(self.x[max_index], region_max),
                    xytext=(self.x[self.anfang], region_max),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))
        ax.legend()
        if created_fig:
            plt.show()
        return self.Spekt.sum() - self.Backround.sum()

def process_peaks(y_spec, x_werte, energy1, energy2, titel1=None, titel2=None, show_plot=True):
    """
    Verarbeitet zwei Peaks (Energien) in den Daten.
    """
    # Berechne die Indizes für die beiden Peaks
    index1 = int(energy1 / Channel)
    index2 = int(energy2 / Channel)
    start_index = min(index1, index2)
    end_index = max(index1, index2)

    # Extrahiere das Intervall der y-Werte zwischen den beiden Energien
    y_interval = y_spec[start_index:end_index+1]

    # Ermittle den zweitniedrigsten eindeutigen Wert als min_y
    unique_sorted = np.sort(np.unique(y_interval))
    if len(unique_sorted) >= 2:
        min_y_value = unique_sorted[1]
    else:
        min_y_value = unique_sorted[0]

    # Erstelle die beiden Intensity-Instanzen
    intens1 = Intensity([y_spec, x_werte], min_y=min_y_value, peak=energy1, titel=titel1)
    intens2 = Intensity([y_spec, x_werte], min_y=min_y_value, peak=energy2, titel=titel2)

    if show_plot:
        fig, ax = plt.subplots()
        netarea1 = intens1.Plot(ax=ax)
        netarea2 = intens2.Plot(ax=ax)
        ax.legend()
        plt.show()
    else:
        netarea1 = intens1.Spekt.sum() - intens1.Backround.sum()
        netarea2 = intens2.Spekt.sum() - intens2.Backround.sum()
        intens1.region_max = np.max(intens1.y[intens1.anfang:intens1.ende+1])
        intens2.region_max = np.max(intens2.y[intens2.anfang:intens2.ende+1])

    max_ratio = intens1.region_max / intens2.region_max if intens2.region_max != 0 else np.nan
    area_ratio = netarea1 / netarea2 if netarea2 != 0 else np.nan

    return max_ratio, area_ratio, intens1.Spekt.sum()/intens2.Spekt.sum()

def process_intervals(y_spec, x_werte, interval1, interval2, titel1=None, titel2=None, show_plot=True):
    """
    Verarbeitet zwei Intervalle in den Daten. Anstelle einzelner Peakenergien werden
    hier Intervalle (als Tupel (Start, Ende) in keV) übergeben. Zur Bestimmung von min_y
    wird der Bereich von der minimalen Start- bis zur maximalen Endenergie beider Intervalle
    betrachtet. Anschließend werden zwei Instanzen der Intensity-Klasse erstellt, die
    ihre Intervalle direkt übernehmen.

    Rückgabe:
      max_ratio, area_ratio, counts_ratio
    """
    # Berechne das Gesamtintervall aus den beiden übergebenen Intervallen:
    start_index = min(int(interval1[0] / Channel), int(interval2[0] / Channel))
    end_index = max(int(interval1[1] / Channel), int(interval2[1] / Channel))
    y_interval = y_spec[start_index:end_index+1]

    # Ermittle den zweitniedrigsten eindeutigen Wert als min_y
    unique_sorted = np.sort(np.unique(y_interval))
    if len(unique_sorted) >= 2:
        min_y_value = unique_sorted[1]
    else:
        min_y_value = unique_sorted[0]

    # Erstelle die Intensity-Instanzen mit direkten Intervallen:
    intens1 = Intensity([y_spec, x_werte], min_y=min_y_value, interval=interval1, titel=titel1,abfallend=True)
    intens2 = Intensity([y_spec, x_werte], min_y=min_y_value, interval=interval2, titel=titel2,abfallend=True)

    if show_plot:
        fig, ax = plt.subplots()
        netarea1 = intens1.Plot(ax=ax)
        netarea2 = intens2.Plot(ax=ax)
        ax.legend()
        plt.show()
    else:
        netarea1 = intens1.Spekt.sum() - intens1.Backround.sum()
        netarea2 = intens2.Spekt.sum() - intens2.Backround.sum()
        intens1.region_max = np.max(intens1.y[intens1.anfang:intens1.ende+1])
        intens2.region_max = np.max(intens2.y[intens2.anfang:intens2.ende+1])

    max_ratio = intens1.region_max / intens2.region_max if intens2.region_max != 0 else np.nan
    area_ratio = netarea1 / netarea2 if netarea2 != 0 else np.nan
    counts_ratio = intens1.Spekt.sum()/intens2.Spekt.sum() if intens2.Spekt.sum() != 0 else np.nan

    return max_ratio, area_ratio, counts_ratio

# Beispielhafter Aufruf für process_intervals:
# Angenommen, x_werte = np.arange(len(y_spec)) * Channel
# y_spec = np.array([...])  # Hier deine Intensitätsdaten
# interval1 = (1.8, 2.2)  # Erstes Intervall (in keV)
# interval2 = (3.8, 4.2)  # Zweites Intervall (in keV)
# max_ratio, area_ratio, counts_ratio = process_intervals(y_spec, x_werte, interval1, interval2,
#                                                         titel1="Intervall 1", titel2="Intervall 2", show_plot=True)
# print("Max Ratio:", max_ratio, "Area Ratio:", area_ratio, "Counts Ratio:", counts_ratio)
