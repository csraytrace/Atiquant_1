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
from Nachbau_ati_sauber.Geoplot_klasse import InteractivePlot


tupel = [(8.692992802969294e-05, 8.139111104249773, 'ta'), (7.043593834104782e-05, 15.746151182987512, 'zr'), (4.787529271299788e-05, 10.540562082673976, 'pb'), (0.00037160975281785234, 2.9833908176471926, 'ag'), (4.1195729328697697e-05, 8.041215748748293, 'cu'), (4.105260140556586e-05, 10.82794806552806, 'bi'), (0.00030177367369520365, 3.1323908092068327, 'cd'), (3.4977055909078095e-05, 8.631189867640346, 'zn'), (0.00017102847840531955, 4.949304535637149, 'v'), (0.00020233169963765473, 4.507980015896446, 'ti')]
#Plot_einfach(tupel).plot_data()


t1 = [(8.692992802969294e-05, 8.139111104249773, 'ta'), (7.043593834104782e-05, 15.746151182987512, 'zr'), (4.787529271299788e-05, 10.540562082673976, 'pb')]

t2 = [[8.692992802969294e-05, 7.043593834104782e-05, 4.787529271299788e-05], [8.139111104249773, 15.746151182987512, 10.540562082673976], ['ta', 'zr', 'pb']]

#Plot_einfach(t1).plot_scatter()
#plt.show()
#Plot_einfach(t2, xy_format=True).plot_scatter()
#plt.show()

plots = []
colors = [
    "blue", "orange", "green", "red", "purple",
    "brown", "pink", "gray", "olive", "cyan",
    "navy", "lime", "teal", "maroon", "gold"
]

            #sigma = 1.36e9 * Z * (U-1)**(1.0314-0.0032*Z + 0.0047 * self.Emax)
            #sigma = 1.35e9 * Z * (U-1)**(1.109-0.00435*Z + 0.00175 * Emax) #loveScott
            #sigma = 1.3844 * 10**9 * Z * (U-1)**(1.05629-0.003492*Z)#Wiederschwinger 1990


#x -y*Z + z*Emax

scott=(1.109, 0.00435, 0.00175)
tube = Röhre(Emax=35 , Röhrenstrom=1, Messzeit=1, step=0.005)
Plot_einfach(tube.Gesamtspektrum_plot).plot_line(log_y=True, color=colors[0], linewidth=0.5,label="Wieder(1.0314,0.0032,0.0047)")
tube = Röhre(Emax=35 , Röhrenstrom=1, Messzeit=1, step=0.005, sigma=scott)
Plot_einfach(tube.Gesamtspektrum_plot).plot_line(log_y=True, color=colors[1], linewidth=0.5,label="Scott(1.109, 0.00435, 0.00175)")

k=1.3
sigmas=[(1.0314*k,0.0032,0.0047),(1.0314,0.0032*k,0.0047),(1.0314,0.0032,0.0047*k)]

for index,i in enumerate(sigmas):
    tube = Röhre(Emax=35, Röhrenstrom=1, Messzeit=1, step=0.005, sigma=i)
   # Plot_einfach(tube.Gesamtspektrum_plot).plot_line(log_y=True, color=colors[index+2], linewidth=0.5,label=str(i))

#for i in range(5):
 #   tube = Röhre(Emax=35 + i, Röhrenstrom=1, Messzeit=1, step=0.05)
 #   Plot_einfach(tube.Gesamtspektrum_plot).plot_line(log_y=True, color=colors[i], linewidth=1,label=str(35+i))

plt.legend()
plt.show()
#plots[0].plot_line(log_y=True, color="y")


#InteractivePlot(plots).show()

#print(tube.Countrate_gesamt)
#print(tube.Countrate_gesamt[0],tube.Countrate_gesamt[1])

#Plot_einfach(tube.Countrate_gesamt).plot_line(log_y=True, color="y")
#Plot_einfach([tube.Röhrenspektrum[0],tube.Röhrenspektrum[1]*20]).plot_line(log_y=True, color="b")
#Plot_einfach(tube.Gesamtspektrum_plot).plot_line(log_y=True, color="b", label="Gesamtspektrum")
# Zeige alle Plots zusammen an
#plt.show()



