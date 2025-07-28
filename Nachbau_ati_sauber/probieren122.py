import numpy as np
from Nachbau_ati_sauber.Calc_I import Calc_I#ohne al, si
from Nachbau_ati_sauber.Element import Element

x=Element(Element="pb")
print(x.Kanten())
print(x.Ubergange())

Elemente = [(150000, 'Ag'), (80000, 'SN')]

Übergänge = [0, 0]

Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (10844, 'AL'), (20692, 'SI'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]

Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


kal_dat = []

for index, i in enumerate(Elemente):
    kal_dat.append([i[1], i[0], Übergänge[index]])
print(kal_dat)

elemente = [entry[0] for entry in kal_dat]
intensität = [entry[1] for entry in kal_dat]

print(elemente)
print(intensität)
print(Übergänge)

Ki = Calc_I()


Ki = Calc_I()

#['sigma=8.0000e-01, Totschicht=0.0000e+00, charzucont_L=1.0000e-01, charzucont=9.5000e-01, Kontaktmaterialdicke=3.0000e+01']


#k=Ki.Kalibrierung_nlls([["Emax"],["Kontaktmaterialdicke"]],
 #                      [[35,45],[10,40]], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge,
 #                      Startwerte=[35, 10],method="lm")


k=Ki.Kalibrierung_nlls([["Einfallswinkelalpha"],["activeLayer"],["Totschicht"],["charzucont_L"],["charzucont"],["Emax"],["Kontaktmaterialdicke"]],
                       [[15,25],[2, 4],[0.0, 0.2],[0.1, 1.2],[0.8, 1.1],[35,45],[10,40]], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge,
                       Startwerte=[15,3,0,1.2,0.95,45,10],method="lm")
print(k)

