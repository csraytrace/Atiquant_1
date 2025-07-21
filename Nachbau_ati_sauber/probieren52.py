import cProfile
import pstats
import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element


Emin = 0
step = 8
step = 0.05
Emax = 24
#Emax = 100
Konzentration=[1]

K = Calc_I(Emax = Emax, Emin=Emin, step=step, Röhrenmaterial="w", Konzentration=Konzentration, P1 = [12])

K.Intensität_alle_jit()
