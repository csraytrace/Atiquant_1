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





path1_k = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,40V\\*.asr'
path1_l = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,40kV,30s_Lline_new\\*.asr'

alle_Daten, alle_Einstellungen = [], []

data = []
Elemente=[]
Übergänge=[]
gemessene_Werte = []

for j in All_asr_files(path1_k):
    Ele = Element(Element=j[0])
    data.append([Ele.K_gemittel_ubergang(), j[1], Ele.Get_Elementsymbol()])
    Elemente.append(Ele.Get_Elementsymbol())
    Übergänge.append(0)
    gemessene_Werte.append(j[1])

for L in All_asr_files(path1_l):
    Ele = Element(Element=L[0])
    data.append([Ele.L_gemittel_ubergang(), L[1], Ele.Get_Elementsymbol()+"_L"])
    Elemente.append(Ele.Get_Elementsymbol())
    Übergänge.append(1)
    gemessene_Werte.append(L[1])

print(Elemente)
print(Übergänge)
print(gemessene_Werte)

alle_Daten.append(data)
print(data)




#Kalibrierung(1, [["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]])

def Minimierung_sqrt(para, para_var, grenzen, gemessene_Intensität, **kwargs):   #Reinelemente
        Startwerte = [np.random.uniform(low, high) for low, high in grenzen]

        def Residuen(gemessene_Intensitäten):
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration) * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)


            return (be_I - gem_I)/be_I**(1/2)

        result = least_squares(
        Residuen,
        Startkonzentration,  # Startwerte für Konzentrationen
        args=( gemessene_Intensitäten,),bounds=(0, np.inf)  # Übergabe des Modells und der gemessenen Daten
        )
        optimized_Konzentration = result.x
        return optimized_Konzentration

