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


def Kalibrierung(para_var, grenzen, stepanzahl, Elemente, Bedingung = False, Speicherort = "test.txt", para = ""):  #stepanzahl >=2, Elemente [[ele,intensität, übergang],[ele2, int2, übergang]...], Bedingung für einfall + ausfallwinkel = 90, para = pa=x, pb=y... oder liste
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

    alle_Daten, alle_Einstellungen = [], []
    for werte in liste:
        parts = []
        for index, x in enumerate(werte):
            parts.append(para_var[index][0] + "=" + f"{x:.4e}")  # Füge jedes Argument hinzu

        if Bedingung:
            for index, x in enumerate(werte):
                if para_var[index][0] == "Einfallswinkelalpha":
                    parts.append("Einfallswinkelbeta" + "=" + f"{90-x:.4e}")
                    break
                if para_var[index][0] == "Einfallswinkelbeta":
                    parts.append("Einfallswinkelalpha" + "=" + f"{90-x:.4e}")
                    break

        Einstellung = ", ".join(parts)
        if (isinstance(para, str) and len(para) > 1):
            Einstellung += ", " + para

        var_einstellung = ", ".join(parts)
        Zähler += 1
        data = []
        if (isinstance(para, list)):
            for index_x, x in enumerate(Elemente):
                if x[2] == 0:
                    Ele = Element(Element=x[0])
                    Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"]"+", " + para[index_x][0])
                    print(Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"]"+", " + para[index_x][0])
                    data.append((Ele.K_gemittel_ubergang(), x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()))
                else:
                    Ele = Element(Element=x[0])
                    Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"],Übergänge=[1]"+", " + para[index_x][0])
                    data.append((Ele.L_gemittel_ubergang(), x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()+"_L"))
        else:
            for x in Elemente:
                if x[2] == 0:
                    Ele = Element(Element=x[0])
                    Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"]")
                    #print(Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"]")
                    data.append((Ele.K_gemittel_ubergang(), x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()))
                    #print(x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
                else:
                    Ele = Element(Element=x[0])
                    Ki = call_class_with_config(Calc_I,Einstellung+", P1=["+str(Ele.Get_Atomicnumber())+"],Übergänge=[1]")
                    data.append((Ele.L_gemittel_ubergang(), x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()+"_L"))
                    #print(x[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])

        print(Einstellung,"Anzahl:",Zähler,"/",Aufrufe)
        alle_Daten.append(data)
        alle_Einstellungen.append([var_einstellung])

    print(alle_Daten)
    print(alle_Einstellungen)
    save_arrays_to_textfile(alle_Daten, alle_Einstellungen, filename=Speicherort)

#Kalibrierung(1, [["Emax"]], [[37,40]])

#Kalibrierung(1, [["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]],1)

##Kalibrierung([["Emax"],["Einfallswinkelalpha"],], [[38,40],[30,40]],[2,2], [["si",50000, 0],[23,50000, 0]], Bedingung = True, para=[["Messzeit = 20"],["Messzeit = 30"]])







