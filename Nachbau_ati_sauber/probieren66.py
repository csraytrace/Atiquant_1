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



Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (11000, 'AL'), (20200, 'SI'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]

#(15300*3, 'AL'), (28600*3, 'SI')

Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


#Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
#, (464025, 'ZN'), (498315, 'GE'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]
#Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

#[44.11640394  1.01304904  0.96859873]

palpha = 25

data = []
for index, ele in enumerate(Elemente):
    x_ele = Element(Element=ele[1])
    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01)
    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

    Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
    #["sigma"],["Totschicht"],["Kontaktmaterialdicke"],["charzucont_L"],["charzucont"]],


    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=44.11640394, Röhrenstrom=0.01, sigma=0.96859873, charzucont=1.01304904,Einfallswinkelalpha=palpha,Einfallswinkelbeta=90-palpha)
    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=44.11640394, Röhrenstrom=0.01, sigma=0.96859873, charzucont=1.01304904,Einfallswinkelalpha=palpha,Einfallswinkelbeta=90-palpha)
    if Übergänge[index] == 0:
        print(ele[0] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
        data.append((x_ele.K_gemittel_ubergang(), ele[0] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], x_ele.Get_Elementsymbol()))

    if Übergänge[index] == 1:
        print(ele[0] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
        data.append((x_ele.L_gemittel_ubergang(), ele[0] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], x_ele.Get_Elementsymbol()+"_L"))




print(data)

Plot_einfach(data, xy_format=False).plot_scatter(abweichung=True,ylabel="Geometriefaktor")
plt.show()


