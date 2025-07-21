import numpy as np
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Emin = 0
step = 8
step = 0.05
Emax = 24
Emax = 100

def Entpacken(werte, step = 0.05, Emin = 0.05):
    add = werte[1]
    x, y = [],[]
    for i in range(len(add)):
        for j in range(len(add[i])):
            if (add[i][j][1] >= 1 and add[i][j][2] > Emin):
                Energie = int(add[i][j][2] / step + Emin / step - 1)
                x.append(Energie*step)
                y.append(add[i][j][1])
    for i in range(len(werte[1][0])):
        if (zahl_zu_string(werte[1][0][i][0]) == " K-L2"):
            K = werte[1][0][i][1]
        if (zahl_zu_string(werte[1][0][i][0]) == " K-M3"):
            L = werte[1][0][i][1]

    print("Verhältnis",K/L)

    return np.array(x),np.array(y)

def Entpacken_sek(werte, step = 0.05, Emin = 0.05):
    add = werte[1]
    x, y = [],[]
    for i in range(len(add)):
        for j in range(len(add[i])):
            if (add[i][j][1] >= 1 and add[i][j][2] > Emin):
                Energie = int(add[i][j][2] / step - Emin / step + 1)
                x.append(Energie*step)
                y.append(add[i][j][1])

    for i in range(len(werte[1][0])):
        if (zahl_zu_string(werte[1][0][i][0]) == " K-L2"):
            K = werte[1][0][i][1]
        if (zahl_zu_string(werte[1][0][i][0]) == " K-M3"):
            L = werte[1][0][i][1]
    print("Verhältnis_sek",K/L)

    return np.array(x),np.array(y),werte[2]
#K = Calc_I(Element_Probe=30, Konzentration=[1,1], P1 = ["pb","Cu"], Übergänge=[1,0], Messzeit=300, Emax=30)

#K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)
#print(K.Intensität_K_alle_jit_fürMinimierung([0.1,0.9]))
#print(K.Intensität_alle_jit())

Konzentration = [1]

print(Element(Element="cu", Emin=Emin, Emax=Emax,step=step).tau[0])
print(Element(Element="mo").Kanten())
print(Element(Element="mo").Ubergange())
print(Element(Element="cu").Ubergange())
print(Element(Element="cu").Kanten())

K_ele = Calc_I(Emax = Emax, Emin=Emin, step=step, Röhrenmaterial="mo", Konzentration=Konzentration, P1 = ["Cu"])
K = Calc_I(Emax = Emax, Emin=Emin, step=step, Röhrenmaterial="w", Konzentration=Konzentration, P1 = ["Cu"])
#print(K.Intensität_K_alle_jit_fürMinimierung([1,1]))
#print(K.Intensität_Sekundärtarget("mo",[1,1]))


#x, y = Entpacken(K.Intensität_alle_jit_fürMinimierung(Konzentration), step, Emin)
x, y = Entpacken(K.Intensität_monoenergetisch([1],17.479))

x_sek, y_sek , anregspek= Entpacken_sek(K.Intensität_Sekundärtarget("mo",Konzentration),step,Emin)
#print(K.Intensität_Sekundärtarget("mo",Konzentration))
#print(np.linspace(0, (len(anregspek) - 1) * 0.05, len(anregspek)))

##plt.plot(np.linspace(0, (len(anregspek) - 1) * step, len(anregspek)), anregspek, label="Anregspek: Sekundärtarget (Mo_char)", linestyle="-", color="gold")

Energie = int(17.48/ step - Emin / step )
Energie_index =(Energie*step)

plt.vlines(x,0, y, color="black", linestyle="-", linewidth=2, label="Cu Monoenergetisch")
##plt.vlines(x_sek+0.2,0, y_sek*max(y)/max(y_sek), color="green", linestyle="-", linewidth=2, label="Cu mit Sekundärtarget Mo")
plt.vlines(Energie_index,0, 3*10**10, color="blue", linestyle="-", linewidth=2, label="Anregspek: Monoenergetisch")

#plt.vlines(x_sek,0, y_sek, color="green", linestyle="-", linewidth=2, label="Cu")
print("Faktor",max(y)/max(y_sek))


plt.ylim(10**4)
plt.title("Anregung", fontsize=16)
plt.xlabel("Energie [keV]", fontsize=12)
plt.ylabel("Counts", fontsize=12)
plt.yscale("log")

plt.legend()  # Legende oben links


# Plot anzeigen
plt.show()
