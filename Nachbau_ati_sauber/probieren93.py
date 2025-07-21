import numpy as np


b = np.array([0.06459316, 0.38480348, 0.0236221, 0., 0.02698127, 0.,
              0., 0., 0., 0., 0., 0., 0., 0., 0.])
l = np.array([7, 66.77832253, 2, 2.69812683])
index_b = [0,1,2,4]



konz_low = b[index_b]

bedingung = l / 100
print(konz_low)
print(bedingung)
print(bedingung>konz_low)
print(konz_low.sum())
konz_low = np.where(bedingung>konz_low,bedingung,konz_low)
print(konz_low.sum())



# Ausgabe des aktualisierten l
print(konz_low)
