from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re

#Verteilung = [0,1,0,0]
#Verteilung = [2,1,0,1]

#Ver="1 H1 + 0 C1 + 0 N1 + 0 O1"

#Ver="100 H1 + 2 C1 + 1 N1 + 3 O1"
#Ver="10 H1 + 5 C1 + 1 N1 + 1 O1"
#Ver="200 H1 + 1 C1 + 0 N1 + 1 O1"

Ver="10 H1 + 6 C1 + 1 N1 + 5 O1"
Ver="10 H1 + 6 C1 + 0 N1 + 5 O1"

#Ver="10 H1 + 1 C1 + 1 N1 + 10 O1"
Verteilung=(Verbindungen_Gewichtsprozent(Ver)[1])
print(Verteilung)
#Verteilung = [0.06714181043095983, 0.39998667821221606, 0.0, 0.5328715113568241]

#Verteilung = [0.12918631240261452, 0.7696069503747024, 0.047244200713654545, 0.05396253650902861]# ["H","C","N","O"]        #in Massenprozent
#Verteilung = [0.0, 0.46160350526558536, 0.5383964947344146, 0.0]


soil_d=554589/1000000
soil_int=445411/1000000
print(soil_int)
print(soil_d)

Verbindung = "47000 Al + 163000 Ca + 25700 Fe + 12100 K + 11300 Mg + 2400 Na + 180000 Si + 3000 Ti + 631 Mn + 51 Rb + 108 Sr + 104 Zn + 13.4 As"
# Zahlen extrahieren und summieren
summe = sum(map(int, re.findall(r"\d+", Verbindung)))
print(re.findall(r"\d+", Verbindung))
print("Gesamtsumme der Zahlen:", summe,1000000-summe)
#Verbindung = "47000 Al1 + 16300 Ca1 + 25700 Fe1 + 12100 K + 11300 Mg1 + 2400 Na1 + 180000 Si1"
ele_soil,kon_soil,z_soil = (Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

print(ele_soil,kon_soil, z_soil)
#Verbindung = "47000 Al1 + 16300 Ca1 + 25700 Fe1 + 12100 K1 + 11300 Mg1 + 2400 Na1 + 180000 Si1 + 3000 Ti1"
#print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))

Elemente = [(0,"H"), (0,"C"), (0,"N"),(0,"O"),       (9302,"Al"), (59419,"Si"),(16117,"K"), (288300,"Ca"), (9484,"Ti"), (7276,"Mn"), (206950,"Fe"), (7015,"Zn"), (9340,"As"),(14433,"Rb"), (19324,"Sr")]    #Mg????, (3000,"Mg")
Übergänge = [0,0,0,0,    0,0, 0, 0,   0,0, 0, 0,    0,0, 0]

#Elemente = [(0,"H"), (0,"C"), (0,"N"),(0,"O"),       (9302,"Al"), (59419,"Si"),(16117,"K"), (288300,"Ca"), (9484,"Ti"), (7276,"Mn"), (206950,"Fe")]    #Mg????, (3000,"Mg")
#Übergänge = [0,0,0,0,    0,0, 0, 0,   0,0, 0, ]


Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])


dark = ["H","C","N","O"]
mg_dark = np.array(normiere_daten(Verteilung)) * 554589

result_str = ""  # Verwende einen anderen Variablennamen für den String

for index, i in enumerate(mg_dark):
    result_str += str(int(i)) + " " + dark[index] + " + "

print(result_str+Verbindung)
#print(Verbindungen_Gewichtsprozent_vonMassenprozent(result_str+Verbindung))

elements,values,z = Verbindungen_Gewichtsprozent_vonMassenprozent(result_str+Verbindung)
#print(elements,values)

#print(result_str+Verbindung)
#summe = sum(map(int, re.findall(r"\d+", (result_str+Verbindung))))
#print(re.findall(r"\d+", result_str+Verbindung))
#print("Gesamtsumme der Zahlen:", summe,1000000-summe)
#formatted_str = " + ".join(f"{value:.3f} {element}" for value, element in zip(values, elements))

#print(formatted_str)

Verteilung=(normiere_daten(Verteilung))

verteil_binder = [0.12918631240261452, 0.7696069503747024, 0.047244200713654545, 0.05396253650902861]
print("SOLL",np.array(verteil_binder)/3)
dark_bounds_lower = np.array([0.12918631240261452, 0.7696069503747024, 0.047244200713654545, 0.05396253650902861])/2

#for index, i in enumerate(Verteilung):
#    Verteilung[index]=(i+ verteil_binder[index])/2

#print(Verteilung)


#(['H', 'C', 'N', 'O'], [0.12918631240261452, 0.7696069503747024, 0.047244200713654545, 0.05396253650902861], 5.509237711718639)
x1,x2,x3=(Verbindungen_Gewichtsprozent("1 C38H76N2O2"))
print(x1,np.array(x2)*100/2,x3)
#  !!!!!!!!Z VON BINDER = 5.509237711718639!!!!!!!!!!!!!
Z_gemittelt = 2/3 * z + 1/3 * 5.509237711718639
#Z_gemittelt += -1
print("Z_gemittelt",Z_gemittelt)

#soil_d=701289/1000000
#soil_int=298711/1000000


print("SOLLWERTE")
#print(dark)
#print(np.array(normiere_daten(Verteilung))*(1-(soil_int*0.5))*100)
print(ele_soil)
sollarray= np.array(kon_soil)*soil_int*2/3*100
formatted_output = " & ".join([f"{val:.3f}" for val in sollarray])
print(formatted_output)

#x,y =(np.array(normiere_daten(Verteilung))*(1-(soil_int*0.5))*(-1)),(np.array(kon_soil)*soil_int*0.5)
#print(x.sum(),y.sum())
#print((1-(soil_int*0.5)))
#print(soil_int*0.5)
#Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)
Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)

#Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=0.3,charzucont=9.46173852e-01)
#Ki = Calc_I(P1 = [ele[1]], Übergänge = [Übergänge[index]], Messzeit=220, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02,charzucont=9.46173852e-01)

######Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=2000, Emax=40, Kontaktmaterialdicke=2.99882970e+01, Totschicht=8.56937060e-11, sigma=8.30349567e-01,charzucont_L=9.17425181e-02*4,charzucont=9.46173852e-01)


#op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati_fix_low( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,binder=[[0.5,0.5],["1C38H76N2O2"]])    #,low_verteilung_volumenprozent=True,
#print(Konzentration)
#print(P1)

for i in range(6):
    Start = np.array([18.34705332e+00,
                      2.47902199e+00, 9.02897017e+00, 6.01036855e-01, 7.89939702e+00,
                      2.21082645e-01, 6.96633268e-02, 1.47809862e+00, 2.56416671e-02,
                      2.44413687e-02, 2.56014989e-02, 3.13641676e-02])

    Start=np.array([8.34705332e+00, 4.97262452e+01, 2.36221004e+00, 1.76801721e+01,2.47902199e+00, 9.02897017e+00, 6.01036855e-01, 7.89939702e+00,2.21082645e-01, 6.96633268e-02, 1.47809862e+00, 2.56416671e-02,2.44413687e-02, 2.56014989e-02, 3.13641676e-02])

    #Start=np.array([8.34705332e+00, 4.97262452e+01, 2.36221004e+00, 1.76801721e+01,2.47902199e+00, 9.02897017e+00, 6.01036855e-01, 7.89939702e+00,2.21082645e-01, 6.96633268e-02, 1.47809862e+00, 2.56416671e-02,2.44413687e-02, 2.56014989e-02, 3.13641676e-02,7.70e-06])

    # Erzeuge zufällige Startwerte mit ähnlicher Größenordnung
    random_Start = 10 ** (np.log10(Start) + np.random.uniform(-1, 1, size=Start.shape))
    #print(random_Start)
    #print(Start)
    #Ki.Minimierung_dark(Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,binder=[[2,1],["1C38H76N2O2"]],Startkonzentration=random_Start.tolist())
    #op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=random_Start.tolist())
    #op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_gemittelt,Startkonzentration=random_Start.tolist())

    #print(Z_gemittelt)



op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,binder=[[2,1],["1C38H76N2O2"]])    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(op_Konz)
Start=[8.34705332e+00, 4.97262452e+01, 2.36221004e+00, 1.76801721e+01,
 2.47902199e+00, 9.02897017e+00, 6.01036855e-01, 7.89939702e+00,
 2.21082645e-01, 6.96633268e-02, 1.47809862e+00, 2.56416671e-02,
 2.44413687e-02, 2.56014989e-02, 3.13641676e-02]
Start = np.append(op_Konz, op_Geo)
Start = op_Konz
Start=Start.tolist()


#Ki.Minimierung_var_Geo_Ati(Z_gemittelt,Startkonzentration=np.append(op_Konz, op_Geo).tolist())
#op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start)

#op_Konz, op_Geo = Ki.Minimierung_frei(Z_mittelwert=Z_gemittelt)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(np.array(Konzentration)[4:]/(Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo)[4:])



#op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start)
#print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(np.array(Konzentration)[4:]/(Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo)[4:])


#print(Start,np.array(Start)*1.1)
print("10")
#op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,10))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,5))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,10))
op_Konz, op_Geo = Ki.Minimierung_frei_ohneZ(Startkonzentration=Start,Bounds_prozent=(Start,15))
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print(np.array(Konzentration)[4:]/(Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo)[4:])
"""



print("20")
op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,20))
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print(np.array(Konzentration)[4:]/(Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo)[4:])
print("40")
op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,40))
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print(np.array(Konzentration)[4:]/(Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo)[4:])

op_Konz, op_Geo = Ki.Minimierung_dark( Z_mittelwert=Z_gemittelt,low_verteilung=Verteilung,binder=[[0.5,0.5],["1C38H76N2O2"]],Z_high_anpassen=False)    #,low_verteilung_volumenprozent=True,

####op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,7))
####print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))



#op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,30))
#op_Konz, op_Geo = Ki.Minimierung_frei(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,40))

#op_Konz, op_Geo = Ki.Minimierung_frei( Z_mittelwert=Z_gemittelt)    #,low_verteilung_volumenprozent=True,
print(Konzentration)
print(P1)

#print(np.array(normiere_daten(op_Konz))*2, op_Geo)
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
#print(x)
#print(x-np.array(Konzentration))
Start = np.append(op_Konz, op_Geo)
Start=Start.tolist()
##print("start",Start)
###op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_gemittelt,Startkonzentration=Start,Bounds_prozent=(Start,30))
###x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

"""


"""
op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_gemittelt,Startkonzentration=Start,binder=[[0.5,0.5],["1C38H76N2O2"]])
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

op_Konz, op_Geo = Ki.Minimierung_var_Geo_Ati(Z_gemittelt,Startkonzentration=Start)
x=((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))

##print(x)
#print(x-np.array(Konzentration))
"""
