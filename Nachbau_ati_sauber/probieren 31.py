import numpy as np

from numba import njit
@njit
def be(liste):
    for i,v in enumerate(liste):
        print(v)

be([1,2,3,2,2,])
