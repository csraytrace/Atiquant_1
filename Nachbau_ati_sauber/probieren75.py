from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

Verbindung = "0.466 Ba1 O1 + 0.45 Ta2 O3 + 0.084 Zn1 O1"
Z_gem = 60.44
Geo = 7.3 * 10**-6

Elemente = [(0, "O"),(6962, "Sr"), (3290, "Zr"), (3123, "Nb"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [0, 0, 0, 0, 0, 1, 1]

#Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
#Übergänge = [0, 0 , 1, 1]

Konzentration = []
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#print(Elemente)
print(Konzentration)
print(P1)
#print("(['Ba', 'O', 'Ta', 'Zn'], [0.2436084974128917, 0.11569639257125641, 0.6197939477694724, 0.020901162246379425], 60.43964005025485)")
#print("([ 'O', 'Zn','Ba', 'Ta'], [0.11569639257125641, 0.020901162246379425, 0.2436084974128917, 0.6197939477694724], 60.43964005025485)")

#(['Ba', 'O', 'Ta', 'Zn'], [0.1391044776119403, 0.5671641791044776, 0.26865671641791045, 0.02507462686567164], 32.69134328358209)

#Ki = Calc_I(Konzentration=Konzentration, P1 = P1,Übergänge=Übergänge,Röhrenstrom=0.02, Messzeit=500, Emax=40)
#print(Ki.Intensität_alle_jit_fürMinimierung([0.11569639257125641, 0.020901162246379425, 0.2436084974128917, 0.6197939477694724])[0]*7.3*10**-6)
#print(Ki.Intensität_alle_jit_fürMinimierung([0.5671641791044776, 0.02507462686567164, 0.1391044776119403, 0.26865671641791045])[0]*7.3*10**-6)

#Ki = Calc_I(Konzentration=Konzentration, P1 = P1,Übergänge=Übergänge,Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)
#print(Ki.Intensität_alle_jit_fürMinimierung([0.11569639257125641, 0.020901162246379425, 0.2436084974128917, 0.6197939477694724])[0]*6.57*10**-6)


Ki = Calc_I(Konzentration=Konzentration, P1=P1, Übergänge=Übergänge, Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)

Geo = 6.79137948809472e-06
op_Konz, op_Geo = Ki.Minimierung_var_Geo(Geo, Z_Gewichtung=5,Z_gemittelt=55.34, Startkonzentration=[50.06451821,  0.30099217,  0.12000271,  0.10465777,  3.41724043, 25.55904962,
 20.4335391 ])

#op_Konz, op_Geo = Ki.Minimierung_var_Geo(Geo, Z_Gewichtung=5, Startkonzentration=[50.06451821,  0.30099217,  0.12000271,  0.10465777,  3.41724043, 25.55904962,
 #20.4335391 ])
print(op_Konz, op_Geo)
print((Ki.Intensität_alle_jit_fürMinimierung(op_Konz)[0]*op_Geo))
print(P1)
print(Gewichtsprozent_Atomprozent(Elemente=P1, Gewichte=op_Konz))



Elemente = [(0, "O"), (63687, "Zn"), (48222, "Ba"), (120547, "Ta")]
Übergänge = [0, 0, 1, 1]
P1 = []
for i in Elemente:
    Konzentration.append(i[0])
    P1.append(i[1])
#Ki = Calc_I(Konzentration=Konzentration, P1=P1,Übergänge=Übergänge,Röhrenstrom=0.02, Messzeit=500, Emax=40, Kontaktmaterialdicke=3.53188106e+01, Totschicht=1.02018852e-03, sigma=8.37582970e-01)
#print(Ki.Intensität_alle_jit_fürMinimierung([0.5671641791044776, 0.02507462686567164, 0.1391044776119403, 0.26865671641791045])[0]*7.3*10**-6)

Verbindung = "0.466 Ba1 O1 + 0.45 Ta2 O3 + 0.084 Zn1 O1"
print(Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindung))
print(Konzentration)
