import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import call_function_with_config
from Nachbau_ati_sauber.packages.Funktionen import call_class_with_config
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
from Nachbau_ati_sauber.Geoplot_klasse import InteractivePlot
from itertools import product
from Nachbau_ati_sauber.Daten_plot_spektrum import save_arrays_to_textfile
from Nachbau_ati_sauber.Daten_plot_spektrum import load_arrays_from_textfile


def Abweichung(geo_list):
    mittelwert = np.array(geo_list).mean()
    abweichung = 0
    for i in geo_list:
        abweichung += abs(i - mittelwert)
    return abweichung / len(geo_list)


pfad="C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Ati_java\\Ati_java\\kalibrierung_test_output.txt"
#pfad="test1.txt"
pfad="testneu.txt"
data, einstellung = load_arrays_from_textfile(pfad)
print(data)
print(einstellung)

Abweichungen = np.array([Abweichung([value[1] for value in i]) for i in data])
sorted_indices = np.argsort(Abweichungen)

print(sorted_indices)


#Plot_einfach(data[0], xy_format=False).plot_scatter(abweichung=True)

#InteractivePlot([Plot_einfach(data[i], xy_format=False) for i in range(len(data))], scatter=True).show()

InteractivePlot(
    [Plot_einfach(data[i], xy_format=False) for i in range(len(data))],
    settings_list=einstellung,  # Einstellungen übergeben
    scatter=True,
    ymin=1*10**-5,
    ymax=5*10**-4,
    color="red",  # Weitere Optionen möglich
    abweichung=True  # Falls benötigt
).show()


#print(einstellung[14])

#plt.show()
