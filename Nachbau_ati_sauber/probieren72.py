from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import Verbindung_einlesen, Filter


Grenzen=[[1.2,0.8],[0.8,1.1]]


Grenzen_i = Grenzen[1]
Grenzen_i.insert(1,(Grenzen_i[0] + Grenzen_i[1]) / 2)


