from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re
from scipy.optimize import least_squares


Elemente = [(0,"O"), (2313, 'Al'), (22272, 'Si'), (9555, 'K'), (11663, 'Ca'), (225121, 'Zn'), (436840, 'Sr'), (134218, 'Cd'), (10733, 'Ba'), (143131, 'Pb')]
Übergänge = [0,0, 0, 0, 0, 0, 0, 0, 1, 1]

Z_gemittelt=22
Verteilung=[1]
Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])

#Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)
#optimized_Konzentration, optimized_Geo = Ki.Minimierung_dark(Z_mittelwert=Z_gemittelt,low_verteilung=[1])
#sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01
Startwerte=[8.30349567e-01,0.3,9.46173852e-01]
lower_bounds = [0.75,0.09,0.5]
upper_bounds = [0.95,0.6,1.2]
Konz = np.array([0.5,0.5,2.9,1.52])
Konz = np.array([ 4 , 19.9 , 3.45 , 3.25 , 3.6 ,  3.86 ,3.85 ,3.87 ,4.1])
def Residuen(params, Konz):

    Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.05, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=params[0],charzucont_L=params[1],charzucont=params[2])

    optimized_Konzentration, optimized_Geo = Ki.Minimierung_dark(Z_mittelwert=Z_gemittelt,low_verteilung=[1])
    print(params)
    print(Konz)
    arr=optimized_Konzentration[1:] / Konz
    result = np.where(arr < 1, 1 / arr, arr)
    print(result.sum())
    print()

    return result

result = least_squares(
    Residuen,
    Startwerte,  # Startwerte für Konzentrationen und Geo
    max_nfev=100,
    args=(Konz,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
    )

print("ergebnis",result.x[:])


####ergebnis [0.76653697 0.16700918 0.69425875]
