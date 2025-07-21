from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element


#Geo = 2.4e-05
#print("Geo:",Geo)

K = Calc_I(Element_Probe=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)
#op_Konz = K.Minimierung(Geo)

#K = Calc_I(Element_Probe=30, Konzentration=[13260, 11176, 850166, 478201, 1672], P1 = [26,28,29,30,50],Übergänge=[0,0,0,0,1], Messzeit=300, Emax=30)

#K = Calc_I(Element_Probe=30,Fensterdicke = 12, Konzentration=[13260, 11176, 850166, 478201, 1672], P1 = [26,28,29,30,50],Übergänge=[0,0,0,0,1], Messzeit=300, Emax=30)

K = Calc_I(charzucont=0.6,activeLayer=4,Kontaktmaterialdicke=30, Konzentration=[13260, 11176, 850166, 478201, 1672, 6883], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=28)

print(K.Intensität_alle_jit())
