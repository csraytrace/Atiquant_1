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


#data = [(22.102955679764456, 2.7974364160346087e-05, 'Ag'), (1.487, 2.008292669486116e-05, 'Al'), (23.10792994876348, 2.8024104846810228e-05, 'Cd'), (8.041215748748293, 2.6601023531216985e-05, 'Cu'), (1.739334980440601, 2.4850581234781094e-05, 'Si'), (4.507980015896446, 3.088955655380787e-05, 'Ti'), (4.949304535637149, 2.9357045523802037e-05, 'V'), (8.631189867640346, 2.7289362849794637e-05, 'Zn'), (15.746151182987512, 2.8447241364671868e-05, 'Zr'), (2.9833908176471926, 4.025639143871985e-05, 'Ag_L'), (10.82794806552806, 2.6179041440619014e-05, 'Bi_L'), (3.1323908092068327, 3.1290301336988714e-05, 'Cd_L'), (10.540562082673976, 2.5001605161335614e-05, 'Pb_L'), (3.443187787468415, 4.0366292128699174e-05, 'Sn_L'), (8.139111104249773, 2.7637953211529504e-05, 'Ta_L')]


#Plot_einfach(data,xy_format=False).plot_scatter(abweichung=True)
#plt.show()


def Kalibrierung(para, para_var, grenzen, stepanzahl):  #stepanzahl >=2
    grenzen_neu = []
    Zähler = 0
    if (isinstance(stepanzahl , (int, float))):
        steps = stepanzahl
        for i in grenzen:
            distanz = (i[1] - i[0]) / (steps-1)
            grenzen_neu.append([i[0] + j * distanz for j in range(steps)])
        liste = list(product(*grenzen_neu))
        Aufrufe = len(liste)
    else:
        for index, i in enumerate(grenzen):
            distanz = (i[1] - i[0])
            grenzen_neu.append([i[0] + x * distanz / (stepanzahl[index] - 1) for x in range(stepanzahl[index])])
        liste = list(product(*grenzen_neu))
        Aufrufe = len(liste)

    path1_k = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,40V\\*.asr'
    path1_l = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,40kV,30s_Lline_new\\*.asr'
    alle_Daten, alle_Einstellungen = [], []
    for werte in liste:
        parts = []
        for index, x in enumerate(werte):
            parts.append(para_var[index][0] + "=" + f"{x:.4e}")  # Füge jedes Argument hinzu


        # Kombiniere die Teile mit ", " und füge den Anfangsteil hinzu
        Einstellung = "Messzeit=30, Röhrenstrom=0.01, " + ", ".join(parts)

        #Einstellung = "Messzeit=30, Röhrenstrom=0.01, Emax=40, " + ", ".join(parts)

        beta = 90 - float(werte[3])
        ##print(beta)
        Einstellung += ", Einfallswinkelbeta=" + str(beta)    ##für einfallswinkel 2
        var_einstellung = ", ".join(parts)
        Zähler += 1
        print(Einstellung,"Anzahl:",Zähler,"/",Aufrufe)
        data = []

        for j in All_asr_files(path1_k):
            Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(j[0])+"]")
            Ele = Element(Element=j[0])
            data.append((Ele.K_gemittel_ubergang(), j[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()))

        for L in All_asr_files(path1_l):
            Ele = Element(Element=L[0])
            Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(L[0])+"],Übergänge=[1]")
            data.append((Ele.L_gemittel_ubergang(), L[1]/Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()+"_L"))

        alle_Daten.append(data)
        alle_Einstellungen.append([var_einstellung])

    print(alle_Daten)
    print(alle_Einstellungen)
    save_arrays_to_textfile(alle_Daten,alle_Einstellungen, filename="stundenrechnung1.txt")

#Kalibrierung(1, [["Emax"]], [[37,40]])

#Kalibrierung(1, [["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]],1)
Kalibrierung(1, [["Emax"],["charzucont"],["sigma"], ["Einfallswinkelalpha"]], [[38,40],[0.4,1],[1.0114,1.0614],[25,40]],[5,5,6,7])

#, sigma = (1.0314,0.0032,0.0047)
# charzucont = 1
#Kalibrierung(1, ["ca","cw","cw"], [[2,2.5],[3,-1],[2,7]])
  #  def __init__(self, Röhrenmaterial = "Rh", Einfallswinkelalpha = 20, Einfallswinkelbeta = 70, Fensterwinkel = 0, charzucont = 1,
      #          Fenstermaterial = "Be", Fensterdicke = 125, Raumwinkel = 1, Röhrenstrom = 0.01, Emin = 0, Emax = 35, sigma = 1.0314,
        #        step=0.05, Messzeit = 30, folder_path='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'):



