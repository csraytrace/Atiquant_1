import numpy as np
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach

def Entpacken(werte, step = 0.05, Emin = 0.05):
    add = werte[1]
    x, y = [],[]
    for i in range(len(add)):
        for j in range(len(add[i])):
            if (add[i][j][1] >= 1 and add[i][j][2] > Emin):
                Energie = int(add[i][j][2] / step + Emin / step - 1)
                x.append(Energie*step)
                y.append(add[i][j][1])
    return np.array(x),np.array(y)

def Entpacken_sek(werte, step = 0.05, Emin = 0.05):
    add = werte[1]
    x, y = [],[]
    for i in range(len(add)):
        for j in range(len(add[i])):
            if (add[i][j][1] >= 1 and add[i][j][2] > Emin):
                Energie = int(add[i][j][2] / step + Emin / step - 1)
                x.append(Energie*step)
                y.append(add[i][j][1])
    return np.array(x),np.array(y),werte[2]


#gemessene Werte

#Ta, La 5470 * 3.12
#zr, Ka 11820 * 2.65
#pb, la 11251 * 1.81
#ag, la 327.56 * 6
#cu, ka 26558 *1.56
#bi, la 10637.8 * 1.7
#cd, la 319 * 6
#zn, ka 30560 * 1.34
#v, ka 7082 * 5.32
#ti, ka 5289 * 6


Proben = ["ta","zr","pb", "ag", "cu", "bi", "cd", "zn", "v", "ti"]
gemessene_int = [5470 * 3.12, 11820 * 2.65, 11251 * 1.81, 327.56 * 6,
                 26558 * 1.56, 10637.8 * 1.7, 319 * 6, 30560 * 1.34, 7082 * 5.32, 5289 * 6]
Übergänge = [1, 0, 1, 1, 0, 1, 1, 0, 0, 0]

x,y = [],[]
Konzentration = [1]
tupel=[]
for index, P1 in enumerate(Proben):
    K = Calc_I(Emax=100, Röhrenmaterial="w", Konzentration=Konzentration, P1=[P1], Übergänge=[Übergänge[index]], Detektormaterial="Ge")
    #print(K.Intensität_Sekundärtarget("mo",Konzentration)[0])
    if Übergänge[index] == 0:
        #print(Element(Element=P1).K_gemittel_ubergang(),gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #x.append(Element(Element=P1).K_gemittel_ubergang())
        #y.append(gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #tupel.append((Element(Element=P1).K_gemittel_ubergang(),gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0],P1))

        if K.Intensität_monoenergetisch([1],17.375)[0][0] != 0:

            tupel.append((Element(Element=P1).K_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.479)[0][0],P1))
            #print(1)
    else:
        #print(Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #x.append(Element(Element=P1).L_gemittel_ubergang())
        #y.append(gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0])
        #tupel.append((Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_Sekundärtarget("mo",Konzentration)[0][0],P1))

        tupel.append((Element(Element=P1).L_gemittel_ubergang(),gemessene_int[index]/K.Intensität_monoenergetisch([1],17.479)[0][0],P1))



#plt.vlines(x,0, y, color="green", linestyle="-", linewidth=2, label="Geo")


#plt.title("Ein einfacher Plot", fontsize=16)
#plt.xlabel("X-Achse", fontsize=12)
#plt.ylabel("Y-Achse", fontsize=12)
#plt.yscale("log")

#plt.legend()  # Legende oben links
print(tupel)

Plot_einfach(tupel, xy_format=False).plot_scatter(abweichung=True, ylabel="Geometriefaktor")

#[[(1.2755978351345261e-05, 22.102955679764456, 'Ag')

# Plot anzeigen
plt.show()

