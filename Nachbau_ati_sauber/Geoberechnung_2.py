import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files


path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.02mA,150s,30V\\*.asr'
path1 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,40V\\*.asr'
path2 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30s,35V\\*.asr'

Pfade = [path, path1, path2]
Röhreneinstellung = [(150,0.02,30), (30, 0.01, 40), (30, 0.01, 35)]


path =  'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,30kV,40s_Lline_new\\*.asr'
path1 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,40kV,30s_Lline_new\\*.asr'
path2 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.01mA,35kV,30s_Lline_new\\*.asr'
path3 = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Alle_Messungen_ASR\\0.02mA,150s,30V_Llinie\\*.asr'
Pfade_L = [path, path1, path2, path3]
Röhreneinstellung_L = [(40,0.01,30), (30, 0.01, 40), (30, 0.01, 35), (150,0.02,30)]
#alle_geo = []

#for i, v in enumerate(Pfade):
 #   a, b, c = Röhreneinstellung[i]
 #   Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c)
 #   for j in All_asr_files(v):
 #       alle_geo.append(Calc.Geometriefaktor_ati_K(j))

#print(alle_geo)
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\blank.txt'
with open(path, 'w') as file:
    file.writelines("")
alle_geo = []
for czuc in np.arange(0.8, 1.25, 0.05):
#for volt in np.arange(-3,1.5,0.5):
    alle_geo = []
    for i, v in enumerate(Pfade):
        a, b, c = Röhreneinstellung[i]

        for j in All_asr_files(v):
            Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc, Element_Probe=j[0])
            #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c + volt, charzucont = 1, Element_Probe=j[0])
            Ele = Element(Element=j[0])
            alle_geo.append((j[1]/Calc.Intensität_K(), Ele.K_gemittel_ubergang(), Ele.Get_Elementsymbol()))
            print(j)
        for L in All_asr_files(Pfade_L[i]):
            a, b, c = Röhreneinstellung_L[i]
            Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc, Element_Probe=L[0])
            #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c + volt, charzucont = 1, Element_Probe=L[0])
            Ele = Element(Element=L[0])
            alle_geo.append((L[1]/Calc.Intensität_L(), Ele.L_gemittel_ubergang(), Ele.Get_Elementsymbol()+"_L"))
            print(L)

        if ( i==0):
            for L in All_asr_files(Pfade_L[3]):
                a, b, c = Röhreneinstellung_L[3]
                Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c, charzucont = czuc, Element_Probe=L[0])
                #Calc = Calc_I(Messzeit = a, Röhrenstrom=b, Emax = c + volt, charzucont = 1, Element_Probe=L[0])
                Ele = Element(Element=L[0])
                alle_geo.append((L[1]/Calc.Intensität_L(), Ele.L_gemittel_ubergang(), Ele.Get_Elementsymbol()+"_L"))
                print(L)

    with open(path, 'a') as file:
        file.writelines("Geometriefaktor mit charzuconst:"+str(czuc)+"\n")
        #file.writelines("Geometriefaktor mit Spannungsänderung:"+str(volt)+"\n")
        file.writelines(str(alle_geo))
        file.writelines("\n")


print(alle_geo)
