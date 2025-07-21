import numpy as np


from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import *
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *

konz_low=[0.2,0.4]
z_low=[1,8]
konz_high=[1,0.4]
z_high=[12,15]
z_gewünscht=9

print(Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht))

print((0.1*1+0.2*8)*1.788079470198675    +  0.6622516556291391*  (0.5*12+15*0.2))

print((0.1+0.2)*1.788079470198675    +  0.6622516556291391*  (0.5+0.2))
