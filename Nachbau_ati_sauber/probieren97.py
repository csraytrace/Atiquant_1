import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
import matplotlib.pyplot as plt


Ver = "66 Li2B4O7 + 34 Li1B1O2"
Ver = "0.14 Si1O2 + 99.6 Al2O3 + 0.005 Ca1O1 + 0.1 Fe2O3 +0.15 Mg1O1"
Ver = "3 Si1 + 0.9 C38H76N2O2"
#Ver = "1 C6H10O5"
#Ver="1 Si1O2"
#Ver="1 al1"
#Ver="1 v1"
#Ver="1 ti1"
#Ver="1 si1"
#Ver = "1 C38H76N2O2"

#Ver="1 H1 + 1 C1 + 2 N1H1 + 1 O1"
#Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])
#print(Verbindung_einlesen(Ver))
#print(Verbindungen_Gewichtsprozent(Ver))
print(Verbindungen_Gewichtsprozent_vonMassenprozent(Ver))
#print(Verbindung_einlesen("H3C1N2O1"))

"""
max_ratio=1/np.array([0.7469304229195088, 3.026666666666667, 3.218241042345277, 0.9171830985915493, 0.8260701889703047, 0.8186195826645265, 0.7390468870099923, 0.4541757443718228])
area_ratio=1/np.array([0.4362716481805799, 3.8363943934267764, 3.558861246473455, 0.6851238887838094, 0.40696582596353315, 0.45120663924580495, 0.3691367351143465, 0.14620454802428984])
area_ratio_mitback=1/np.array([0.49543374351672936, 2.047072967724036, 1.8401078790213832, 0.6539725532683279, 0.47816201859229746, 0.5099504902436657, 0.4566322568621157, 0.2847602283031952])

x=[14,22,23,13,10.80458010185401,7.468644393629722,10.655788151261717,6.764105747271824]

Plot_einfach([x,max_ratio], xy_format=True).plot_scatter(ylabel="Geometriefaktor")
plt.show()
Plot_einfach([x,area_ratio], xy_format=True).plot_scatter(ylabel="Geometriefaktor")
plt.show()
Plot_einfach([x,area_ratio_mitback], xy_format=True).plot_scatter(ylabel="Geometriefaktor")
plt.show()

"""
