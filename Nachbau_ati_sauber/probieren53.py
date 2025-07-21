import numpy as np
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *



#K = Calc_I( Konzentration=[1,1], P1 = ["H","Cu"])
K = Calc_I(Emax = 100, Röhrenmaterial="w",Konzentration=[1,1], P1 = ["H","Cu"])

x=K.Intensität_K_alle_jit_fürSekundärtarget(["mo"], [1])

x = x.astype(object)
for i in range(len(x[:,:,0])):
    for index, j in enumerate(x[:,:,0][i]):
        x[:,:,0][i][index] = zahl_zu_string(x[:,:,0][i][index])
alle_Übergänge=[[], []]
for i in range(len(x[:,:,0])):
    for index, j in enumerate(x[:,:,0][i]):
        if (x[:,:,1][i][index]!=0):
            alle_Übergänge[0].append(x[:,:,1][i][index])
            alle_Übergänge[1].append(x[:,:,2][i][index])

alle_Übergänge=np.array(alle_Übergänge)

#print("alte",x)

##K.Intensität_Sekundärtarget(Sekundärtarget="mo 1 cd 1")[:, :, 2]

#for i in K.Intensität_Sekundärtarget(Sekundärtarget="mo 1 cd 1")[:, :, 2]:
 #   for j in i:
  #      print(j)


#print((K.Intensität_K_alle_jit_fürSekundärtarget(["Cd"], [1]))[:,:,1])
x_Ele = Element(Element="pb")


tube = Röhre(Emax = 100,Röhrenmaterial="w")
tube_sek = Röhre(Röhrenmaterial="mo",Emax = 100)

sek_tube = np.array(tube_sek.Char_spec)
#print(sek_tube)
#print(sek_tube[:,0],sek_tube[:,1])

plt.vlines(sek_tube[:,0].astype(float),0, sek_tube[:,1].astype(float), color="black", linestyle="-", linewidth=2, label="Sekundärtarget_aus_Tube")

plt.plot(tube.Countrate_gesamt[0], tube.Countrate_gesamt[1], label="Röhrenspektrum", linestyle="-", color="green")


verhältnis = max(np.array(sek_tube[:,1].astype(float)))/max(alle_Übergänge[0])
# Plot erstellen
plt.vlines(alle_Übergänge[1]+0.1,0, alle_Übergänge[0]*verhältnis, color="blue", linestyle="-", linewidth=2, label="Sekundärtarget")  # Linie mit Markern

#print(alle_Übergänge[1],alle_Übergänge[0])
# Titel und Achsenbeschriftungen
plt.title("Ein einfacher Plot", fontsize=16)
plt.xlabel("X-Achse", fontsize=12)
plt.ylabel("Y-Achse", fontsize=12)
plt.yscale("log")

plt.legend()  # Legende oben links


# Plot anzeigen
plt.show()
