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
from numba import njit
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

#print(Verbindung_einlesen("ca"))
#print(Verbindung_einlesen("ca 1 mo 2"))
#print(Verbindung_einlesen("ca1mo2"))
print(Filter("cu 1 cd 1",0.05,24))
print(Filter("luft",1,3))
print(Filter("luft",1,4.4))

Dateipfad = 'C:\\Users\\julia\\OneDrive\\Dokumente' \
              '\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'

#x = (Filter_array(Material="cu", Dicke=0.0001, Emin=0.2, Emax=30, step=0.1, Dateipfad=Dateipfad, Dichte = None, Fenstereinfallwinkel=0))

#print(x)
#Plot_einfach(x).plot_line()
#    def __init__(self, Röhrenmaterial = "Rh", Einfallswinkelalpha = 20, Einfallswinkelbeta = 70, Fensterwinkel = 0, charzucont = 1,
     #           Fenstermaterial = "Be", Fensterdicke = 125, Raumwinkel = 1, Röhrenstrom = 0.01, Emin = 0, Emax = 35, sigma = 1.0314,
      #          step=0.05, Messzeit = 30, folder_path='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'):




plots=[]

tube = Röhre(sigma = 1.0314)
plots.append(Plot_einfach(Röhre(charzucont=4.0000e-01, sigma=1.0114e+00, Einfallswinkelalpha=4.0000e+01).Röhrenspektrum))
plots.append(Plot_einfach(Röhre(sigma = 1.0314).Röhrenspektrum))
plots.append(Plot_einfach(Röhre(sigma = 1.0314).Röhrenspektrum))
plots.append(Plot_einfach(Röhre(sigma = 1.0214).Röhrenspektrum))
plots.append(Plot_einfach(Röhre(sigma = 1.0414).Röhrenspektrum))


k = 10
plots.append(Plot_einfach(Röhre(Einfallswinkelalpha=k, Einfallswinkelbeta=90-k).Röhrenspektrum))
k = 20
plots.append(Plot_einfach(Röhre(Einfallswinkelalpha=k, Einfallswinkelbeta=90-k).Röhrenspektrum))
k = 30
plots.append(Plot_einfach(Röhre(Einfallswinkelalpha=k, Einfallswinkelbeta=90-k).Röhrenspektrum))
k = 40
plots.append(Plot_einfach(Röhre(Einfallswinkelalpha=k, Einfallswinkelbeta=90-k).Röhrenspektrum))
InteractivePlot(
    plots,
    settings_list="einstellung",  # Einstellungen übergeben
    color="red",  # Weitere Optionen möglich
).show()
