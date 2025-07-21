import numpy as np
import ast
from Nachbau_ati_sauber.Geoplot_klasse import PlotSwitcher

def Geo_liste(array):
    geo_list = []
    for i in array:
        geo_list.append(i[0])
    return np.array(geo_list)

def x_werte(array):
    geo_list = []
    for i in array:
        geo_list.append(i[1])
    return np.array(geo_list)

def Abweichung(geo_list):
    mittelwert = geo_list.mean()
    abweichung = 0
    for i in geo_list:
        abweichung += abs(i - mittelwert)
    return abweichung / len(geo_list)

geometriefaktoren = []
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo.txt'
#path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_volt.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_mit_L_volt_new.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_auf_linie.txt'
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Geometriefaktoren\\Geo_volt_all.txt'
with open(path, 'r') as file:
  #  with open(path, 'r') as file:
        for line in file:
            if (line[0]=="["):
                print(line.strip("\n"))
                geometriefaktoren.append(ast.literal_eval(line))
y_werte = []

for i in geometriefaktoren:
        array = Geo_liste(i)
        y_werte.append(array)

x_werte = x_werte(geometriefaktoren[0])

#datasets = [(x_werte, y_werte[0]), (x_werte, y_werte[1]), (x_werte, y_werte[2])]

#for i in range(len(y_werte)):
 #   y_werte[i][4] *=  10
 #   y_werte[i][14] *=  10
 #   y_werte[i][24] *=  10

datasets = (x_werte, y_werte)

#print(geometriefaktoren)
#print(geometriefaktoren[0])
#print(geometriefaktoren[1])
#print(len(geometriefaktoren))
#print(geometriefaktoren)
#print(len(geometriefaktoren[0]))
for i in range(len(geometriefaktoren[0])):
    if (i == 0):
        zeichen = geometriefaktoren[0][0][2]
    else:
        if (zeichen == geometriefaktoren[0][i][2]):
            zahl = i
            break

print(zahl)
plot_switcher = PlotSwitcher(geometriefaktoren)
