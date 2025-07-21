from Nachbau_ati_sauber.Element import Element
import numpy as np
#def A(zahl):
 #   return str(f"{zahl:.3f}")
def A(wert):
    if wert<=0:
        return"-"
    wert="{:.2e}".format(wert)
    return wert


def Prozent(wert):
    if wert is None or wert <= 0:
        return "-\t"
    else:
        return "{:.1f}\t".format(wert*100)

Energie_array = [1.5, 3, 3.5318, 3.56, 3.7273, 3.7571, 3.9904, 4, 4.0224, 5, 6, 8, 10, 15, 20, 26.663, 26.876, 30, 40, 50]
x = Element(Element="Cd")

#Energie_array = [1, 1.5, 2, 2.391, 2.410, 2.491, 2.511, 2.942, 2.965, 3, 3.407, 3.434, 3.678, 3.707, 4, 5, 6, 8, 10, 12.65, 12.75, 14.73, 14.85, 15, 15.32, 15.45, 20, 30, 40, 50, 60, 80]#für element 81
Energie_array = [1, 1.5, 2, 2.4861, 2.5060, 2.592, 2.6128, 3, 3.0514, 3.0758, 3.5464, 3.5748, 3.8233, 3.8539, 4, 5, 6, 8, 10, 13.026, 13.13, 15, 15.236, 15.358, 15.841, 15.968, 20, 30, 40, 50, 60]
Energie_array = [3, 3.0514, 3.0758, 3.5464, 3.5748, 3.8233, 3.8539, 4, 5, 6, 8, 10, 13.026, 13.13, 15, 15.236, 15.358, 15.841, 15.968, 20, 30, 40, 50, 60]
x = Element(Element = "Pb")
print("Energie", "\t", "Tau", "\t", "Tau_K", "\t", "Tau_L1", "\t", "Tau_L2", "\t", "Tau_L3")
for Energie in Energie_array:
    print(A(Energie), "\t", A(x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()), "\t", A(x.S_ij(" K", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()),
           "\t", A(x.S_ij("L1", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()), "\t",    A(x.S_ij("L2", Energie)
        * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()), "\t",     A(x.S_ij("L3", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()))

###################LOCHTRANSFERFAKTOR
print()
print("Energie", "\t", "Tau", "\t", "Tau_L1", "\t", "Tau_L2", "\t", "Tau_L3")
for Energie in Energie_array:
    print(A(Energie), "&", A(x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()),
           "&", A(x.S_ij("L1", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()), "&",    A(x.S_ij("L2", Energie)
        * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()*x.Löcherübertrag_L2_Energie(Energie)), "&",     A(x.S_ij("L3", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()*x.Löcherübertrag_L3_Energie(Energie)))

arrayL = np.array(
    [0]*39 + [
        0, 0, 3.205e4,
        0, 0, 2.22e4,
        0, 0, 2.13e4,
        0, 1.38e4, 2.085e4,
        0, 1.305e4, 1.92e4,
        6.9631e3, 1.27e4, 1.88e4,
        4.72e3, 7.17e3, 9.96e3,
        2.16e3, 2.39e3, 3e3,
        1.19e3, 1.06e3, 1.25e3,
        7.32e2, 5.59e2, 6.24e2,
        4.85e2, 3.28e2, 3.51e2,
    ]
)

array_tau=np.array([
    6.72e5, 6.45e5, 7.3e5, 5.14e5, 5.345e5, 455e5, 4.665e5, 4.273e5, 2.484e5, 1.5822e5, 7.66e4, 4.322e4, 2.175e4,
    5.33e4, 3.72e4, 3.572e4, 4.884e4, 4.5288e4, 5.128e4, 2.888e4, 9.9289e3, 4.592e3, 2.508e3, 1.525e3
])


def replace_zeros_with_minus_one(arr):
    arr = np.array(arr)  # falls es noch kein numpy-Array ist
    arr[arr == 0] = -1
    return arr

arrayL = replace_zeros_with_minus_one(arrayL)

print()
print()
print()
print("Energie", "\t", "Tau", "\t", "Tau_L1", "\t", "Tau_L2", "\t", "Tau_L3")
for index,Energie in enumerate(Energie_array):
    print(A(Energie), "&", Prozent(x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g() / array_tau[index]),
           "&", Prozent(x.S_ij("L1", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g() / arrayL[index * 3]), "&",    Prozent(x.S_ij("L2", Energie)
        * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()/ arrayL[index * 3 + 1]), "&",     Prozent(x.S_ij("L3", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()/ arrayL[index * 3 + 2]),"\\\\")

