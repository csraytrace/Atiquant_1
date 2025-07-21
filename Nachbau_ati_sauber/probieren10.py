import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element

from numba import jit

x_Element = Element(Element = "cd")
print(x_Element.Ubergange())
print(x_Element.Kanten())
Kalkulation = Calc_I(Element_Probe="ag", Fensterdicke_det=12)



#Kalkulation.Primärintensität()

#Kalkulation.Geometriefaktor_ati_K(("Ag",1111))
#Kalkulation.Sekundäranregung(("Ag",1111))

#Kalkulation = Calc_I(Element_Probe="ag", Fensterdicke_det=12)
#Kalkulation.Intensität_K()


#Kalkulation = Calc_I(Element_Probe=50,  Fensterdicke_det=12)
#print(9549/Kalkulation.Intensität_L())
#print(9549/Kalkulation.Intensität_K())





