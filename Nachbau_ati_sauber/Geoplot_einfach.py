import numpy as np
import ast
from Nachbau_ati_sauber.Geoplot_klasse import PlotSwitcher


geometriefaktoren = []
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_volt.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_mit_L.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_mit_L_volt.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_mit_L_volt_new.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_volt_all.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_czuc_all.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_auf_linie.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_czuc_all_neuesL.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_neu.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_auf_linie_1.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_auf_linie_2.txt'#prozentuell

path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\Original.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\-2Volt_0.6char.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\-2Volt_0.6char_4al.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\-2Volt_0.6char_4al_kontakt30.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\0.95Volt.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\-2Volt.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\0.6char.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Für Prä\\Original_ohne_LTF.txt'
with open(path, 'r') as file:
  #  with open(path, 'r') as file:
        for line in file:
            if (line[0]=="["):
                print(line.strip("\n"))
                geometriefaktoren.append(ast.literal_eval(line))


#for i in range(len(geometriefaktoren)):
#   geometriefaktoren[i][11] = (geometriefaktoren[i][11][0]*0.85,geometriefaktoren[i][11][1],geometriefaktoren[i][11][2])
 #   geometriefaktoren[i][24] = (geometriefaktoren[i][24][0]*0.85,geometriefaktoren[i][24][1],geometriefaktoren[i][24][2])
 #   geometriefaktoren[i][37] = (geometriefaktoren[i][37][0]*0.85,geometriefaktoren[i][37][1],geometriefaktoren[i][37][2])

print(path.split("\\"))

#plot_switcher = PlotSwitcher(geometriefaktoren)

savefig = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Präsentation\\neue Plots\\' + path.split("\\")[-1]
print("will",geometriefaktoren)
plot_switcher = PlotSwitcher(geometriefaktoren,savefig[:-3]+"PNG")
