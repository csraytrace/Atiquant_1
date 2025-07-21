import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files


path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.02mA,150s,30V\\*.asr'
path1 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.01mA,30s,40V\\*.asr'
path2 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.01mA,30s,35V\\*.asr'
Pfade = [path, path1, path2]
Röhreneinstellung = [(150,0.02,30), (30, 0.01, 40), (30, 0.01, 35)]
#alle_geo = []

#for i, v in enumerate(Pfade):
 #   a, b, c = Röhreneinstellung[i]
 #   Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c)
 #   for j in All_asr_files(v):
 #       alle_geo.append(Calc.Geometriefaktor_ati_K(j))

#print(alle_geo)
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_1.txt'
with open(path, 'w') as file:
    file.writelines("")
alle_geo = []
for czuc in np.arange(0.8, 1.25, 0.05):
#for volt in np.arange(-3,1.5,0.5):
    alle_geo = []
    for i, v in enumerate(Pfade):
        a, b, c = Röhreneinstellung[i]
        Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc)
        #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c + volt, charzucont = 1)
        for j in All_asr_files(v):
            alle_geo.append(Calc.Geometriefaktor_ati_K(j))
    with open(path, 'a') as file:
        file.writelines("Geometriefaktor mit charzuconst:"+str(czuc)+"\n")
        #file.writelines("Geometriefaktor mit Spannungsänderung:"+str(volt)+"\n")
        file.writelines(str(alle_geo))
        file.writelines("\n")


print(alle_geo)
