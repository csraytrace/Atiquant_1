import numpy as np
import matplotlib.pyplot as plt

Channel = 0.02

class Intensity():
    def __init__(self, spec, min_y=100, peak=None, titel=None):
        self.y, self.x = np.array(spec[0]), np.array(spec[1])
        if peak is not None:
            self.anfang = int(peak / Channel)
            self.ende = int(peak / Channel)
        else:
            self.anfang = peak
            self.ende = peak
        self.titel = titel
        self.min_y = min_y
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

    def Plot(self, ax=None):
        created_fig = False
        if ax is None:
            fig, ax = plt.subplots()
            created_fig = True
        #label = "Netarea: " + str(self.Spekt.sum() - self.Backround.sum())
        label = "Netarea: " + str(self.Spekt.sum()) +"-" +str(self.Backround.sum())
        # Gesamtspektrum plotten
        ax.plot(self.x, self.y, color="g", label=label)
        # Bereichsgrenzen (Anfang/Ende) markieren
        ax.axvline(x=self.anfang * Channel, color='r', linestyle='--', label='Anfang')
        ax.axvline(x=self.ende * Channel, color='r', linestyle='--', label='Ende')
        # Balken für Signal und Hintergrund zeichnen
        ax.bar(self.x[self.anfang:self.ende+1], self.Spekt, width=Channel, align='center')
        ax.bar(self.x[self.anfang:self.ende+1], self.Backround, width=Channel, align='center', color="r")
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

    def Balken(self):
        # Berechnet einen linearen Hintergrund im Peak-Bereich
        k = (self.y[self.ende] - self.y[self.anfang]) / (self.ende - self.anfang + 1)
        if self.y[self.ende] / self.y[self.anfang] < 1:
            k = (self.y[self.anfang] - self.y[self.ende]) / (self.ende - self.anfang + 1) * (-1)
        gesamtzahl = []
        abzug = []
        for i in range(self.ende - self.anfang + 1):
            gesamtzahl.append(self.y[self.anfang + i])
            abzug.append(int(self.y[self.anfang] + k * i))
        self.Spekt = np.array(gesamtzahl)
        self.Backround = np.array(abzug)

def process_peaks(y_spec, x_werte, energy1, energy2, titel1=None, titel2=None, show_plot=True):
    """
    Verarbeitet zwei Peaks (Energien) in den Daten:
      - Es wird im Intervall zwischen den beiden Peak-Energien der zweitniedrigste y-Wert als min_y bestimmt.
      - Zwei Instanzen der Klasse Intensity werden erstellt.
      - Optional werden beide Peaks in einem gemeinsamen Plot dargestellt.
      - Es werden zwei Verhältnisse berechnet:
          * max_ratio: Verhältnis der Maximalwerte (Peakhöhen)
          * area_ratio: Verhältnis der Netto-Flächen der Peaks

    Parameter:
      y_spec   : Array mit Intensitätswerten
      x_werte  : Array mit Energie-Werten (z.B. np.arange(len(y_spec)) * Channel)
      energy1  : Erste Energie (Peak)
      energy2  : Zweite Energie (Peak)
      titel1   : Optionaler Titel für den ersten Peak
      titel2   : Optionaler Titel für den zweiten Peak
      show_plot: Boolean, ob der Plot angezeigt werden soll (default: True)

    Rückgabe:
      max_ratio, area_ratio
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
        # Erstelle eine gemeinsame Figur und Achse, wenn geplottet werden soll
        fig, ax = plt.subplots()
        netarea1 = intens1.Plot(ax=ax)
        netarea2 = intens2.Plot(ax=ax)
        ax.legend()
        plt.show()
    else:
        # Falls kein Plot angezeigt werden soll, berechne die Netto-Flächen direkt
        netarea1 = intens1.Spekt.sum() - intens1.Backround.sum()
        netarea2 = intens2.Spekt.sum() - intens2.Backround.sum()
        # Zusätzlich werden die Maxima in den Bereichen ermittelt
        intens1.region_max = np.max(intens1.y[intens1.anfang:intens1.ende+1])
        intens2.region_max = np.max(intens2.y[intens2.anfang:intens2.ende+1])

    # Berechne die beiden Verhältnisse
    max_ratio = intens1.region_max / intens2.region_max if intens2.region_max != 0 else np.nan
    area_ratio = netarea1 / netarea2 if netarea2 != 0 else np.nan

    return max_ratio, area_ratio, intens1.Spekt.sum()/intens2.Spekt.sum()

# Beispielhafter Aufruf:
# Angenommen, x_werte = np.arange(len(y_spec)) * Channel
# y_spec = np.array([...])  # Hier deine Intensitätsdaten
# energy1 = 2.0    # Erster Peak bei 2.0 keV
# energy2 = 4.0    # Zweiter Peak bei 4.0 keV
# max_ratio, area_ratio = process_peaks(y_spec, x_werte, energy1, energy2,
#                                        titel1="Peak 1", titel2="Peak 2", show_plot=True)
# print("Max Ratio:", max_ratio, "Area Ratio:", area_ratio)
