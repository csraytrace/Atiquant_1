import cProfile
import pstats
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

def main():
    for i in range(10):
        Kalkulation = Calc_I(Element_Probe="Cd",  Fensterdicke_det=12)
        Kalkulation.Intensität_L()
        print(i)
    #Kalkulation = Calc_I(Element_Probe=50,  Fensterdicke_det=12)
    #Kalkulation = Calc_I(Element_Probe=50,  Fensterdicke_det=12)
    #print(9549/Kalkulation.Intensität_L())



if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
