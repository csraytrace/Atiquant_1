import numpy as np

def BeerLambert(Massenschwachungskoe, Dichte, Dicke, Phi = 0):
    if (Phi == None):
        print("none")
    return np.exp(-Massenschwachungskoe * Dichte * Dicke / np.cos(Phi * np.pi / 180))


print(BeerLambert(1,1,1))
