import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.Röhre_veränderbar import Röhre_veränderbar
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files


#tube = Röhre_veränderbar(charzucont = 1)
tube = Röhre(step = 0.05)
tube1 = Röhre_veränderbar(charzucont = 1, step = 0.01)

x_werte,y_werte = tube.Countrate_gesamt
x_werte,y_werte = tube.Röhrenspektrum

plt.plot(x_werte,y_werte,color="b", label='spekt')

x_werte,y_werte = tube1.Countrate_gesamt
x_werte,y_werte = tube1.Röhrenspektrum

plt.plot(x_werte,y_werte,color="g", label='spekt')

print(tube.Char_spec)


Charspek = tube.Charstrahlung()

x_values = [item[0] for item in Charspek]
y_values = [item[1] for item in Charspek]

# Plotten der vertikalen Linien
#plt.vlines(x=x_values, ymin=[0]*len(y_values), ymax=y_values, color='blue', alpha=0.7)

Charspek = tube1.Charstrahlung()

x_values = [item[0] for item in Charspek]
y_values = [item[1] for item in Charspek]

# Plotten der vertikalen Linien
#plt.vlines(x=x_values, ymin=[0]*len(y_values), ymax=y_values, color='green', alpha=0.7)


plt.xlabel('Energie [keV]')
plt.ylabel('Geometriefaktor')
#plt.legend()
plt.show()
