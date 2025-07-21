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
from scipy.optimize import least_squares


K = Calc_I(Emax=100, Röhrenmaterial="w", P1=["ca"], Detektormaterial="Ge")

Proben = ['Ag', 'Al', 'Cd', 'Cu', 'Si', 'Ti', 'V', 'Zn', 'Zr', 'Ag', 'Bi', 'Cd', 'Pb', 'Sn', 'Ta']
Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
gemessene_Werte = [56428, 20390, 45350, 247414, 40824, 120441, 139393, 263279, 248458, 11088, 55591, 9611, 54091, 14212, 47623]
#para_var, grenzen, gemessene_Intensität, Elemente, Übergänge
s=K.Kalibrierung_nlls([["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]], gemessene_Werte, Proben, Übergänge)
#s=K.Kalibrierung_nlls([["Emax"]], [[37,40]], gemessene_Werte, Proben, Übergänge)
print(s)
#Kalibrierung(1, [["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]])



