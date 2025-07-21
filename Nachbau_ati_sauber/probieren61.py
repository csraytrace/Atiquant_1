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

#Proben = ["ta","zr","pb", "ag", "cu", "bi", "cd", "zn", "v", "ti"]
#gemessene_int = [5470 * 3.12, 11820 * 2.65, 11251 * 1.81, 327.56 * 6,
#                 26558 * 1.56, 10637.8 * 1.7, 319 * 6, 30560 * 1.34, 7082 * 5.32, 5289 * 6]
#Übergänge = [1, 0, 1, 1, 0, 1, 1, 0, 0, 0]

Proben = ["ag", "cd", "ti"]
Übergänge = [1, 1, 0]
gemessene_int = [2000, 2200, 13800 * 4]

Proben = ["ag", "cd", "ti", "V", "Ta", "Cu"]
Übergänge = [1, 1, 0, 0, 1, 0]
gemessene_int = [183800, 210000, 5240900, 7192000, 5500000, 30000000]
#27740000
Dicke_Luft = 0.5
Moly = Element(Element="mo")

print(Moly.Ubergange())

x,y = [],[]
Konzentration = [1]
tupel=[]
for index, P1 in enumerate(Proben):
    K = Calc_I(Emax=40, Röhrenmaterial="rh", Konzentration=Konzentration, P1=[P1], Übergänge=[Übergänge[index]], Detektormaterial="si",Bedeckungsfaktor=0, Fensterdicke_det=12.7, activeLayer=0.5)
    if Übergänge[index] == 0:
        #tupel.append((Element(Element=P1).K_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.375)[0][0],P1))

        tupel.append((Element(Element=P1).K_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.479)[0][0] / Filter("luft",Dicke=Dicke_Luft, Energie=Element(Element=P1).K_gemittel_ubergang()),P1+"_luft"))
        print(Filter("luft",Dicke=Dicke_Luft, Energie=Element(Element=P1).K_gemittel_ubergang()),P1+"_luft")
        print(K.Intensität_monoenergetisch([1],17.375)[0])
    else:
        #print(Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #x.append(Element(Element=P1).L_gemittel_ubergang())
        #y.append(gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #tupel.append((Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.375)[0][0],P1))

        tupel.append((Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.375)[0][0] / Filter("luft",Dicke=Dicke_Luft, Energie=Element(Element=P1).L_gemittel_ubergang()),P1+"_luft"))
        print(Filter("luft",Dicke=Dicke_Luft, Energie=Element(Element=P1).L_gemittel_ubergang()),P1+"_luft")



print(tupel)
Plot_einfach(tupel,xy_format=False).plot_scatter(abweichung=True)
plt.show()
