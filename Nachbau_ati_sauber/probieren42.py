from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np


print("mein Gedanke")
Geo = 3.4e-05
K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)

print("mein Gedanke")
Geo = 3.1e-05
K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)

print("mein Gedanke")
Geo = 3e-05
K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)

print("mein Gedanke")
Geo = 2.8e-05
K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)
op_Konz = K.Minimierung_sqrt_zusatz(Geo, Z_gemittelt=31.5125, Z_Gewichtung=1)
