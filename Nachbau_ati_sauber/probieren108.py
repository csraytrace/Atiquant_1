


"""


Konzentration = params[:]
Konzentration = normiere_daten(Konzentration)
konz_low = low_kon_be(Konzentration[0],low_verteilung)

konz_high = Konzentration[1:]

new_low, new_high = (Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert))

Konzentration[1:]*=new_high
Konzentration[0]*=new_low


neue_Konz = np.concatenate((low_kon_be(Konzentration[0],low_verteilung), Konzentration[1:]))

berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(neue_Konz, vorbereitete_Werte)[0]

berechnete_Intensitäten *= self.Geo_IbIg(berechnete_Intensitäten,index_high)

Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)

return (be_I - gem_I)
"""
