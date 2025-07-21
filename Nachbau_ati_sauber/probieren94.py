import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
import matplotlib.pyplot as plt
    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

    #Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

tube_original = Röhre(Messzeit=220, Emax=40, Röhrenstrom=0.01,step=0.005)
tube_alt = Röhre(sigma=8.37582970e-01,Messzeit=220, Emax=40, Röhrenstrom=0.01,step=0.005)
tube_neu = Röhre(sigma=8.30349567e-01,Messzeit=220, Emax=40, Röhrenstrom=0.01,step=0.005,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

print(tube_alt.Gesamtspektrum_plot)


#Plot_einfach(tube_alt.Gesamtspektrum_plot, xy_format=True).plot_line(ylabel="Geometriefaktor")
Plot_einfach(tube_original.Gesamtspektrum_plot, xy_format=True).plot_line(ylabel="Counts", label="Wiederschwinger-Modell",log_y=True,title="Vergleich-Röhrenspektrum")
Plot_einfach(tube_neu.Gesamtspektrum_plot, xy_format=True).plot_line(ylabel="Counts",color="r",label="neue_Röhreneinstellung",log_y=True,ymin=10**9,ymax=10**13,title="Vergleich-Röhrenspektrum")
plt.legend()
plt.show()
