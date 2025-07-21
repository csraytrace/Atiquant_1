import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files

def Umschreiben(wert):
    if(wert<=0):
        return "-"
    else:
        wert="{:.2e}".format(wert)
        return wert


def Prozent(wert):
    if wert is None or wert <= 0:
        return "-"
    else:
        return "{:.1f}".format(wert*100)

#array für höherenergetische Elemente
werte = np.array([
    1.04e-1, 0, 4.72e-2, 0, 4.53e-3, 0, 2.10e-3, 0,
    1.70e-1, 0, 7.70e-2, 0, 7.50e-3, 0, 3.50e-3, 0,
    2.8e-1, 0, 1.28e-1, 0, 1.27e-2, 0, 5.93e-3, 0,
    4.19e-1, 0, 1.92e-1, 0, 1.93e-2, 0, 9.06e-3, 0,
    6.41e-1, 0, 2.96e-1, 0, 3.01e-2, 0, 1.42e-2, 0,
    8.94e-1, 0, 4.15e-1, 0, 4.27e-2, 0, 2.02e-2, 0,
    1.2, 0, 5.61e-1, 0, 5.85e-2, 0, 2.78e-2, 0,
    1.78, 0, 8.37e-1, 0, 9.84e-2, 0, 4.22e-2, 0,
    2.45e+0, 0, 1.16e0, 0, 1.24e-1, 0, 5.93e-2, 0,
    3.04e0, 4.91e-4, 1.44e0, 2.4e-4, 1.56e-1, 3.02e-5, 7.5e-2, 1.55e-5,
    3.88e+00, 1.36e-03, 1.85e+00, 6.65e-04, 2.03e-01, 9.36e-05, 9.76e-02, 4.28e-05,
    4.90e+00, 2.95e-03, 2.35e+00, 1.43e-03, 2.60e-01, 1.77e-04, 1.26e-01, 9.05e-05,
    6.39e+00, 5.28e-03,3.07e+00, 2.57e-03, 3.45e-01, 3.18e-04, 1.67e-01, 1.62e-04,
    7.85e+00, 8.17e-03,3.80e+00, 3.96e-03, 4.31e-01, 4.88e-04, 2.10e-01, 2.48e-04,
    9.84e+00, 1.21e-02,4.78e+00, 5.86e-03, 5.49e-01, 7.20e-04, 2.68e-01, 3.66e-04,
    1.17e+01, 1.65e-02,5.73e+00, 7.98e-03, 6.65e-01, 9.80e-04, 3.26e-01, 4.98e-04,
    1.46e+01, 2.34e-02,7.16e+00, 1.13e-02, 8.42e-01, 1.37e-03, 4.13e-01, 6.96e-04,
    1.66e+01, 2.96e-02,9.18e+00, 1.42e-02, 9.72e-01, 1.72e-03, 4.79e-01, 8.69e-04,
    1.95e+01, 3.62e-02,9.57e+00, 1.74e-02, 1.16e+00, 2.11e-03, 5.73e-01, 1.07e-03,
    2.18e+01, 4.14e-02,1.09e+01, 1.99e-02, 1.32e+00, 2.36e-03, 6.53e-01, 1.19e-03,
    2.46e+01, 5.36e-02,1.23e+01, 2.58e-02, 1.51e+00, 3.12e-03, 7.51e-01, 1.58e-03,
    2.77e+01, 6.33e-02,1.39e+01, 3.04e-02, 1.73e+00, 3.67e-03, 8.60e-01, 1.85e-03,
    3.03e+01, 7.62e-02,1.53e+01, 3.57e-02, 1.92e+00, 4.41e-03, 9.58e-01, 2.23e-03,
    3.43e+01, 9.48e-02, 1.74e+01, 4.55e-02, 2.21e+00, 5.46e-03, 1.11e+00, 2.76e-03,
    3.72e+01, 1.13e-01, 1.90e+01, 5.42e-02, 2.43e+00, 6.54e-03, 1.22e+00, 3.30e-03,
    4.11e+01, 1.33e-01, 2.11e+01, 6.24e-02, 2.74e+00, 6.95e-03, 1.38e+00, 3.42e-03,
    4.49e+01, 1.60e-01, 2.32e+01, 7.66e-02, 3.04e+00, 9.09e-03, 1.54e+00, 4.57e-03,
    4.88e+01, 1.89e-01, 2.54e+01, 9.04e-02, 3.37e+00, 1.07e-02, 1.71e+00, 5.39e-03,
    0, 2.25e-01, 2.76e+01, 1.08e-01, 3.72e+00, 1.28e-02, 1.89e+00, 6.47e-03,
    0, 2.82e-01, 3.00e+01, 1.36e-01, 4.08e+00, 1.66e-02, 2.09e+00, 8.44e-03,
    0, 3.25e-01, 3.20e+01, 1.57e-01, 4.41e+00, 1.92e-02, 2.25e+00, 9.77e-03,
    0, 3.71e-01, 3.39e+01, 1.79e-01, 4.73e+00, 2.17e-02, 2.42e+00, 1.11e-02,
    0, 4.25e-01, 3.61e+01, 2.06e-01, 5.11e+00, 2.50e-02, 2.63e+00, 1.27e-02,
    0.00e+00, 4.80e-01, 0.00e+00, 2.32e-01, 5.53e+00, 2.81e-02, 2.85e+00, 1.42e-02,
    0.00e+00, 5.32e-01, 0.00e+00, 2.57e-01, 5.86e+00, 3.13e-02, 3.03e+00, 1.59e-02,
    0.00e+00, 5.99e-01, 0.00e+00, 2.90e-01, 6.31e+00, 3.52e-02, 3.27e+00, 1.78e-02,
    0.00e+00, 6.69e-01, 0.00e+00, 3.23e-01, 6.56e+00, 3.93e-02, 3.44e+00, 1.99e-02,
    0.00e+00, 7.56e-01, 0.00e+00, 3.66e-01, 7.00e+00, 4.46e-02, 3.65e+00, 2.27e-02,
    0.00e+00, 6.69e-01, 0.00e+00, 3.12e-01, 7.32e+00, 3.41e-02, 3.83e+00, 1.67e-02,
    0.00e+00, 7.67e-01, 0.00e+00, 3.60e-01, 7.69e+00, 3.91e-02, 4.03e+00, 1.91e-02,
    0.00e+00, 8.48e-01, 0.00e+00, 3.98e-01, 7.87e+00, 4.36e-02, 4.14e+00, 2.13e-02,
    0.00e+00, 9.81e-01, 0.00e+00, 4.62e-01, 9.49e+00, 5.05e-02, 4.48e+00, 2.47e-02,
    0.00e+00, 1.10e+00, 0.00e+00, 5.18e-01, 8.80e+00, 5.69e-02, 4.65e+00, 2.79e-02,
    0.00e+00, 1.25e+00, 0.00e+00, 5.91e-01, 9.28e+00, 6.51e-02, 4.91e+00, 3.19e-02,
    0.00e+00, 1.38e+00, 0.00e+00, 6.55e-01, 9.55e+00, 7.24e-02, 5.07e+00, 3.55e-02,
    0.00e+00, 1.58e+00, 0.00e+00, 7.50e-01, 1.00e+01, 8.37e-02, 5.35e+00, 4.12e-02,
    0.00e+00, 1.80e+00, 0.00e+00, 9.57e-01, 1.05e+01, 9.57e-02, 5.66e+00, 4.69e-02,
    0.00e+00, 2.04e+00, 0.00e+00, 9.71e-01, 1.11e+01, 1.09e-01, 6.00e+00, 5.34e-02,
])
def replace_zeros_with_minus_one(arr):
    arr = np.array(arr)  # falls es noch kein numpy-Array ist
    arr[arr == 0] = -1
    return arr

werte = replace_zeros_with_minus_one(werte)

Energie = 17.44
Energie = 22.5
Energie = 47
Energien = [17.44, 22.5, 47, 59.54]
#Energien = [4.55, 5.46, 7, 8.13]
#Energien = [4.55, 5.46, 7, 8.13]
Kante = " K"
K_übergänge = [" K-L1", " K-L2", " K-L3"]
Start_Element = 12
End_Element = 70
End_Element = 59

#Element_x = Element(Element = 22)
#Element_x.S_ij(Kante,Energie) * Element_x.Massenabsorptionskoeffizient(Energie) * Element_x.Ubergange()
#print(Element_x.Ubergange())
K_tau = []
L_tau = []
#print("Energie:",Energie, r"Ka")
for j in range(Start_Element, End_Element):
    Element_x = Element(Element = j)

    for k in Energien:
        tau = 0
        Energie = k
        for i in Element_x.Ubergange():
            if (i[0] in K_übergänge):
                tau += Element_x.S_ij(Kante,Energie) * Element_x.Massenabsorptionskoeffizient(Energie)[1][0] * i[2] * Element_x.Omega_Schale(Kante)
                #print(Element_x.S_ij(Kante,Energie) , Element_x.Massenabsorptionskoeffizient(Energie)[1][0] , i[2] , Element_x.Omega_Schale(Kante))
        #print(j,Element_x.Get_Elementsymbol(),"\tTau:", round(tau,2))
        K_tau.append(tau)
        #print(tau)

L_übergänge = ["L3-M4", "L3-M5"]
Kante = "L3"

#print("Energie:",Energie, r"La")
print()
for j in range(Start_Element, End_Element):
    Element_x = Element(Element = j)
    for k in Energien:
        tau = 0
        Energie=k
        for i in Element_x.Ubergange():
            if (i[0] in L_übergänge):
                #tau += Element_x.S_ij(Kante,Energie) * Element_x.Massenabsorptionskoeffizient(Energie)[1][0] * i[2] * Element_x.Omega_Schale(Kante) #ohne Lochtransfer
                tau += Element_x.S_ij(Kante,Energie) * Element_x.Massenabsorptionskoeffizient(Energie)[1][0] * i[2] * Element_x.Omega_Schale(Kante) * Element_x.Löcherübertrag_L3_Energie(Energie)


                #print(Element_x.S_ij(Kante,Energie) , Element_x.Massenabsorptionskoeffizient(Energie)[1][0] , i[2] , Element_x.Omega_Schale(Kante))
        #print(j,Element_x.Get_Elementsymbol(),"\tTau:", round(tau*10**2,2),"E-02")
        L_tau.append(tau)



#print(L_tau)
start=1

##for i in range(Start_Element, End_Element):
 ##   Element_x = Element(Element=i)

##    #print(i, Element_x.Get_Elementsymbol(),"\t",Umschreiben(K_tau[(i-Start_Element)*4]),"\t", Umschreiben(L_tau[(i-Start_Element)*4]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+3]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+3]))
 ##   print(i,"&", Element_x.Get_Elementsymbol(),"&",Umschreiben(K_tau[(i-Start_Element)*4]),"&", Umschreiben(L_tau[(i-Start_Element)*4]),"&", Umschreiben(K_tau[(i-Start_Element)*4+1]),"&", Umschreiben(L_tau[(i-Start_Element)*4+1]),"&", Umschreiben(K_tau[(i-Start_Element)*4+2]),"&", Umschreiben(L_tau[(i-Start_Element)*4+2]),"&", Umschreiben(K_tau[(i-Start_Element)*4+3]),"&", Umschreiben(L_tau[(i-Start_Element)*4+3]),"\\\\")
 ##   if (start%4==0):
  ##      print("\\midrule")

  ##  start+=1




start=1
index=0
for i in range(Start_Element, End_Element):
    Element_x = Element(Element=i)

    #print(i, Element_x.Get_Elementsymbol(),"\t",Umschreiben(K_tau[(i-Start_Element)*4]),"\t", Umschreiben(L_tau[(i-Start_Element)*4]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+3]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+3]))
    print(i,"&", Element_x.Get_Elementsymbol(),"&",Prozent(K_tau[(i-Start_Element)*4] / werte[(index * 8)]),"&", Prozent(L_tau[(i-Start_Element)*4] / werte[(index * 8 + 1)]),"&", Prozent(K_tau[(i-Start_Element)*4+1] / werte[(index * 8 + 2)]),"&", Prozent(L_tau[(i-Start_Element)*4+1] / werte[(index * 8 + 3)])
          ,"&", Prozent(K_tau[(i-Start_Element)*4+2] / werte[(index * 8 + 4)]),"&", Prozent(L_tau[(i-Start_Element)*4+2] / werte[(index * 8 + 5)]),"&", Prozent(K_tau[(i-Start_Element)*4+3] / werte[(index * 8 + 6)]),"&", Prozent(L_tau[(i-Start_Element)*4+3] / werte[(index * 8 + 7)]),"\\\\")
    if (start%4==0):
        print("\\midrule")
    #print("k1",werte[(index * 8)], "index",(index * 8))

    start+=1
    index+=1

""""""
#Originalwerte
start=1
index=0
for i in range(Start_Element, End_Element):
    Element_x = Element(Element=i)

    #print(i, Element_x.Get_Elementsymbol(),"\t",Umschreiben(K_tau[(i-Start_Element)*4]),"\t", Umschreiben(L_tau[(i-Start_Element)*4]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+1]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+2]),"\t", Umschreiben(K_tau[(i-Start_Element)*4+3]),"\t", Umschreiben(L_tau[(i-Start_Element)*4+3]))
    print(i,"&", Element_x.Get_Elementsymbol(),"&",Umschreiben(werte[(index * 8)]),"&", Umschreiben(werte[(index * 8 + 1)]),"&", Umschreiben(werte[(index * 8 + 2)]),"&", Umschreiben(werte[(index * 8 + 3)])
          ,"&", Umschreiben( werte[(index * 8 + 4)]),"&", Umschreiben(werte[(index * 8 + 5)]),"&", Umschreiben(werte[(index * 8 + 6)]),"&", Umschreiben( werte[(index * 8 + 7)]),"\\\\")
    if (start%4==0):
        print("\\midrule")
    #print("k1",werte[(index * 8)], "index",(index * 8))

    start+=1
    index+=1




