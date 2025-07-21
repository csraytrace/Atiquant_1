from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.Element import Element
import numpy as np

def Prozent(array):
    return (" & ".join([f"{value*100:.2f}" for value in array])+"\\\\")

def Elemente_auskunft(array):
    for i in array:
        x_Ele = Element(Element = i)
        print("Elementsymbol:",x_Ele.Get_Elementsymbol(), "Ordnungszahl:",x_Ele.Get_Atomicnumber())


def Intensitäten(array):
    print((" & ".join(["{:.2e}".format(value) for value in array])+"\\\\"))


