import numpy as np
from Nachbau_ati_sauber.Calc_I import Calc_I#ohne al, si

Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]
Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (10844, 'AL'), (20692, 'SI'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]

Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]




kal_dat = []

for index, i in enumerate(Elemente):
    kal_dat.append([i[1], i[0], Übergänge[index]])
para = "Messzeit=220, Röhrenstrom=0.01"
print(kal_dat)

elemente = [entry[0] for entry in kal_dat]
intensität = [entry[1] for entry in kal_dat]

print(elemente)
print(intensität)
print(Übergänge)

Ki = Calc_I()
#Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01, Einfallswinkelalpha=25,Einfallswinkelbeta=65)


#k=Ki.Kalibrierung_nlls([["Emax"],["charzucont"], ["Einfallswinkelalpha"], ["sigma"]], [[42,46],[0.9,1.2],[10,35],[0.9,1.0514]], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge, Startwerte=[44,1,1.0114], para="Messzeit=220, Röhrenstrom=0.01, Einfallswinkelalpha=25,Einfallswinkelbeta=65")
#print(k)

#k=Ki.Kalibrierung_nlls([["Emax"],["charzucont"], ["Einfallswinkelalpha"], ["sigma"]], [[42,46],[0.9,1.2],[10,35],[0.9,1.0514]], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge, Startwerte=[44,1,25,1.0114], para="Messzeit=220, Röhrenstrom=0.01", Bedingung=True)
##k=Ki.Kalibrierung_nlls([["sigma"],["Totschicht"], ["Kontaktmaterialdicke"]], [[0.83,1],[0,0.2],[35,45],], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge, Startwerte=[0.85,0.01,40], para="Messzeit=220, Röhrenstrom=0.01, Emax=40")
#print(kal_dat[0:2])
#Kalibrierung([["Emax"],["charzucont"], ["Einfallswinkelalpha"], ["sigma"]], [[39,44],[0.3,1],[10,35],[1.0114,1.0514]],[5,6,6,5], kal_dat, Bedingung = True, Speicherort = "test.txt", para = para)
#s=K.Kalibrierung_nlls([["Emax"],["charzucont"],["sigma"]], [[37,40],[0.6,1],[1.0214,1.0414]], gemessene_Werte, Proben, Übergänge)

para = "Messzeit=220, Röhrenstrom=0.01, Emax=40"

Ki = Calc_I(Messzeit=220, Röhrenstrom=0.01, Emax=40)

#['sigma=8.0000e-01, Totschicht=0.0000e+00, charzucont_L=1.0000e-01, charzucont=9.5000e-01, Kontaktmaterialdicke=3.0000e+01']

k=Ki.Kalibrierung_nlls([["sigma"],["Totschicht"],["Kontaktmaterialdicke"],["charzucont_L"],["charzucont"]], [[0.75,0.9],[0,0.1],[25,40],[0.05,0.2],[0.9,1]], gemessene_Intensität=intensität, Elemente=elemente, Übergänge=Übergänge, Startwerte=[0.8,0,30,0.1,0.95], para="Messzeit=220, Röhrenstrom=0.01, Emax=40")
print(k)

