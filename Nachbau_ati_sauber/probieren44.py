from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np

Konzentration=[9460, 6089, 830759, 516707, 684, 6670]
K = Calc_I(Element_Probe=30, Konzentration=[9460, 6089, 830759, 516707, 684, 6670], P1 = [26,28,29,30,50,82],Übergänge=[0,0,0,0,1,1], Messzeit=300, Emax=30)

Konz = K.Intensität_alle_jit()
x = (K.Intensität_alle_jit_fürMinimierung(Konz)[0])
for index,i in enumerate(x):
    print(Konzentration[index]/i)



Geo = 2.7151364588867653e-05
op_Konz = [ 0.44118553,  0.29317123, 60.20144212, 35.54526424,  0.67894652,  2.83999037]
#print(((K.Intensität_K_alle_jit_fürMinimierung(op_Konz)*Geo)))

#print(K.Minimierung(Geo))
#K.Minimierung_res_neu(Geo)
#K.Minimierung_sqrt_zusatz(Geo)
