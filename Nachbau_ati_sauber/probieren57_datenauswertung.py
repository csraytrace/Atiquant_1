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


Emin = 0
step = 8
step = 0.05
Emax = 24
Emax = 100
Konzentration=[1]

path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.02mA,150s,30V\\*.asr'
path1 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,40V\\*.asr'
path2 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,35V\\*.asr'

#Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc, Element_Probe=j[0])
Pfade = [path, path1, path2]
Einstellung = [["Messzeit=150, Röhrenstrom=0.02, Emax=30"], ["Messzeit=30, Röhrenstrom=0.01, Emax=40"], ["Messzeit=30, Röhrenstrom=0.01, Emax=35"]]


path1_k = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,40V\\*.asr'
Einstellung_k = "Messzeit=30, Röhrenstrom=0.01, Emax=40"

path1_l = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,40kV,30s_Lline_new\\*.asr'
Einstellung_l = "Messzeit=30, Röhrenstrom=0.01, Emax=40"

#K = Calc_I(Messzeit=150, Röhrenstrom=0.02, Emax=30, P1=[47])
#K.Intensität_alle_jit()

#for i, v in enumerate(Pfade):
  #  for j in All_asr_files(v):
        #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc, Element_Probe=j[0])
        #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c + volt, charzucont = 1, Element_Probe=j[0])
    ###    Ele = Element(Element=j[0])
        #alle_geo.append((j[1]/Calc.Intensität_K(), Ele.K_gemittel_ubergang(), Ele.Get_Elementsymbol()))
        ##print(Einstellung[i][0]+", P1=["+str(j[0])+"]")
   ###     Ki = call_class_with_config(Calc_I,Einstellung[i][0]+", P1=["+str(j[0])+"]")
        #print(Ki.Intensität_K_alle_jit_fürMinimierung([1])[0])
        #print(j[1])
    ###    print((j[1]/Ki.Intensität_K_alle_jit_fürMinimierung([1])[0][0], Ele.K_gemittel_ubergang(), Ele.Get_Elementsymbol()))
#print(v)
data = []
for j in All_asr_files(path1_k):
    Ki = call_class_with_config(Calc_I,Einstellung_k+", P1=["+str(j[0])+"]")
    Ele = Element(Element=j[0])
    #print((j[1]/Ki.Intensität_K_alle_jit_fürMinimierung([1])[0][0], Ele.K_gemittel_ubergang(), Ele.Get_Elementsymbol()))
    data.append((Ele.K_gemittel_ubergang(), j[1] / Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()))
    print("k")

for L in All_asr_files(path1_l):
    Ele = Element(Element=L[0])
    Ki = call_class_with_config(Calc_I,Einstellung_k+", P1=["+str(L[0])+"],Übergänge=[1]")
    #print(L[1]/Ki.Intensität_K_alle_jit_fürMinimierung([1])[0][0], Ele.L_gemittel_ubergang(), Ele.Get_Elementsymbol()+"_L")
    data.append((Ele.L_gemittel_ubergang(), L[1]/Ki.Intensität_alle_jit_fürMinimierung([1])[0][0], Ele.Get_Elementsymbol()+"_L"))
    print("l")

print(data)
Plot_einfach(data, xy_format=False).plot_scatter(abweichung=True)

plt.legend()
plt.show()




