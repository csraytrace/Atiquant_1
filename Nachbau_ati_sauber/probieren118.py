from Nachbau_ati_sauber.Calc_I import Calc_I
import numpy as np
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
import re


x=Element(Element=30)
print(x.Get_McMaster())
print(x.Jumps())
print(x.Kanten())
print(x.Ubergange())
