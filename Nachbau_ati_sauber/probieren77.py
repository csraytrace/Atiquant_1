import numpy as np
from Nachbau_ati_sauber.Element import Element

def berechne_neue_konzentrationen(konz_low, z_low, konz_high, z_high, z_gewünscht):

    konz_sum_low = sum(konz_low)
    konz_sum_high = sum(konz_high)
    z_mittel_low = sum(np.array(konz_low) * np.array(z_low)) / konz_sum_low
    z_mittel_high = sum(np.array(konz_high) * np.array(z_high)) / konz_sum_high

    konz_gesamt = konz_sum_low + konz_sum_high
    konz_sum_low /= konz_gesamt
    konz_sum_high /= konz_gesamt

    Zb = z_mittel_low * konz_sum_low + z_mittel_high * konz_sum_high

    #konz_neu_high = ((konz_sum_low * z_mittel_low) / z_gewünscht - konz_sum_low) / (1 - (z_mittel_high / z_mittel_low))
    #konz_neu_low = ((konz_sum_high * z_mittel_high / z_gewünscht - konz_sum_high) / (1 - (z_mittel_low / z_mittel_high)))

    #Zg=55.34
    konz_neu_low = ((z_gewünscht - z_mittel_high) / (z_mittel_low - z_mittel_high))
    konz_neu_high = 1 - konz_neu_low
    print(konz_neu_low,konz_neu_high)
    print(konz_sum_low,konz_sum_high)
    konz_gesamt_neu = konz_neu_high + konz_neu_low
    konz_neu_low /= konz_gesamt_neu
    konz_neu_high /= konz_gesamt_neu
    #print(z_mittel_low,z_mittel_high, konz_sum_low, konz_sum_high, konz_neu_high,konz_neu_low)

    return konz_neu_low / konz_sum_low,  konz_neu_high / konz_sum_high

# Beispielwerte
konz_low = [50.06451821]
z_low = [8]
konz_high = [0.30099217,  0.12000271,  0.10465777,  3.41724043, 25.55904962,
 20.4335391 ]
z_high = [38, 40, 41, 30, 56, 73]
z_gewünscht = 55.34


#konz_low = [50.06451821 *0.10677110088783483]
#z_low = [8]
#konz_high = np.array([0.30099217,  0.12000271,  0.10465777,  3.41724043, 25.55904962,
# 20.4335391 ])*0.8932288991121652
#z_high = [38, 40, 41, 30, 56, 73]
#z_gewünscht = 55.34

# Berechnung der neuen Konzentrationen
konz_neu_low, konz_neu_high = berechne_neue_konzentrationen(konz_low, z_low, konz_high, z_high, z_gewünscht)

print(f"Neue Konzentration für Z < 11: {konz_neu_low:.4f}")
print(f"Neue Konzentration für Z > 11: {konz_neu_high:.4f}")

Z=[]
for e in ['O', 'Sr', 'Zr', 'Nb', 'Zn', 'Ba', 'Ta']:
    Z.append(Element(Element=e).Get_Atomicnumber())


print(Z)
['O', 'Sr', 'Zr', 'Nb', 'Zn', 'Ba', 'Ta']

l = 50.06451821

k = np.array([0.30099217,  0.12000271,  0.10465777,  3.41724043, 25.55904962,
 20.4335391 ])*konz_neu_high
print(l * konz_neu_low,k, k.sum() )
