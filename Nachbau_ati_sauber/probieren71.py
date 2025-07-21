from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import Verbindung_einlesen, Filter


#Verbindung="Ce1S1Cu1"
print("Start")


#Ki = Calc_I(P1=["Fe", "Ni", "Cu", "Zn", "Sn", "Pb"], Konzentration=[9460, 6089, 830759, 516707, 684, 6670], Messzeit=300, Emax=30, Übergänge=[0,0,0,0,1,1])
#Ki.Atiquant()
#Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01, Einfallswinkelalpha=25,Einfallswinkelbeta=65,P1=Verbindung_einlesen(Verbindung)[0], Konzentration=Verbindung_einlesen(Verbindung)[1], Emax=40, Übergänge=[1,0,0])
#Ki.Atiquant()
palpha=25

Konzentration=[2518, 2283, 251200, 171500, 1158, 3104]
Übergänge=[0,0,0,0,0,1]
Ki = Calc_I(P1=["Fe", "Ni", "Cu", "Zn", "Sn", "Pb"], Konzentration=Konzentration, Messzeit=220, Übergänge=Übergänge, Emax=44.11640394, Röhrenstrom=0.01, sigma=0.96859873, charzucont=1.01304904,Einfallswinkelalpha=palpha,Einfallswinkelbeta=90-palpha)

ret, geo = Ki.Atiquant()
print("Sollwerte","[0.26, 0.15, 59.27, 35.72, 0.88, 3.73]")
print(ret*100)
print("sollint", Ki.Intensität_alle_jit_fürMinimierung([0.26, 0.15, 59.27, 35.72, 0.88, 3.73])[0]*geo)


Ki = Calc_I(P1=["Fe", "Ni", "Cu", "Zn", "Sn", "Pb"], Konzentration=Konzentration, Messzeit=220, Übergänge=Übergänge, Emax=44, Röhrenstrom=0.01)

ret = Ki.Atiquant()
print("Sollwerte","[0.26, 0.15, 59.27, 35.72, 0.88, 3.73]")
print(ret[0]*100)
print("sollint", Ki.Intensität_alle_jit_fürMinimierung([0.26, 0.15, 59.27, 35.72, 0.88, 3.73])[0]*geo)

Ki = Calc_I(P1=["Fe", "Ni", "Cu", "Zn", "Sn", "Pb"], Konzentration=Konzentration, Messzeit=220, Übergänge=Übergänge, Emax=40, Röhrenstrom=0.01)

ret = Ki.Atiquant()
print("Sollwerte","[0.26, 0.15, 59.27, 35.72, 0.88, 3.73]")
print(ret[0]*100)

print("sollint", Ki.Intensität_alle_jit_fürMinimierung([0.26, 0.15, 59.27, 35.72, 0.88, 3.73])[0]*geo)


Ki = Calc_I(P1=["Fe", "Ni", "Cu", "Zn", "Sn", "Pb"], Konzentration=Konzentration, Messzeit=220, Übergänge=Übergänge, Emax=40, Röhrenstrom=0.01, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

ret = Ki.Atiquant()
print("Sollwerte","[0.26, 0.15, 59.27, 35.72, 0.88, 3.73]")
print(ret[0]*100)

print("sollint", Ki.Intensität_alle_jit_fürMinimierung([0.26, 0.15, 59.27, 35.72, 0.88, 3.73])[0]*geo)
