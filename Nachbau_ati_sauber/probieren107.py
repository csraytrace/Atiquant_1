from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re
z_low=[1 ,6, 7,3]
z_high=[15, 16,19, 20 ]
z_gewünscht=6.72114052
for i in range(10):

    random_floats = np.random.rand(8)

    konz_low=random_floats[:4]
    konz_high=random_floats[4:]

    print(Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht))
    random_floats=normiere_daten(random_floats)
    konz_low=random_floats[:4]
    konz_high=random_floats[4:]

    print(Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht))
    print()




print(Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht))

print(normiere_daten([34, 25, 12,23,55 ,2, 1  ]))

konz_low=[0.2236842105263158, 0.16447368421052633, 0.07894736842105263]
z_low=[1 ,6, 7]
konz_high=[0.1513157894736842, 0.3618421052631579, 0.013157894736842105, 0.006578947368421052]
z_high=[15, 16,19, 20 ]
z_gewünscht=6.72114052

print(Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht))
