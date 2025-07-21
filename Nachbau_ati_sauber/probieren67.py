from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
import matplotlib.pyplot as plt
from probieren65_kalibrierung import Kalibrierung
data = [(22.102955679764456, 9.464380149237125e-06, 'Ag'), (25.19196900066341, 9.62872891884464e-06, 'Sn'), (4.507980015896446, 5.700638469840015e-06, 'Ti'), (23.10792994876348, 9.376039111927535e-06, 'Cd'), (8.041215748748293, 6.3496649053085695e-06, 'Cu'), (4.949304535637149, 5.63955836067385e-06, 'V'), (15.746151182987512, 8.50292147272477e-06, 'Zr'), (8.631189867640346, 6.558690381535779e-06, 'Zn'), (9.876462210974347, 6.787205509992707e-06, 'Ge'), (1.487, 2.9014989437051454e-06, 'Al'), (1.739334980440601, 1.5698459205553556e-06, 'Si'), (10.82794806552806, 6.857377846241864e-06, 'Bi_L'), (3.1323908092068327, 5.947232007505139e-06, 'Cd_L'), (3.443187787468415, 6.660236798401273e-06, 'Sn_L'), (10.540562082673976, 6.872761629973381e-06, 'Pb_L'), (8.139111104249773, 6.547759503569299e-06, 'Ta_L'), (2.9833908176471926, 6.554931899948976e-06, 'Ag_L')]


Plot_einfach(data, xy_format=False).plot_scatter(abweichung=True)
#plt.show()


Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (10844, 'AL'), (20692, 'SI'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]

Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

#ohne al, si
#Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
#, (464025, 'ZN'), (498315, 'GE'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]
#Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


##Elemente = [(140000, 'Ag'), (66746, 'SN')]
##Übergänge = [0, 0,]

kal_dat = []

for index, i in enumerate(Elemente):
    kal_dat.append([i[1], i[0], Übergänge[index]])
para = "Messzeit=220, Röhrenstrom=0.01"
para=""
print(kal_dat)
#Kalibrierung([["Emax"],["charzucont"], ["Einfallswinkelalpha"], ["sigma"]], [[39,44],[0.3,1],[10,35],[1.0114,1.0514]],[5,6,6,5], kal_dat, Bedingung = True, Speicherort = "test.txt", para = para)
##para = "Messzeit=220, Röhrenstrom=0.01, Emax=40"
#Kalibrierung([["sigma"],["Totschicht"],["charzucont_L"],["charzucont"],["Kontaktmaterialdicke"]], [[0.8,1],[0,0.02],[0,0.2],[0.8,1.1],[30,40]],[3,2,5,3,2], kal_dat, Speicherort = "test1.txt", para = para)
##Kalibrierung([["Einfallswinkelalpha"],["Kontaktmaterialdicke"]], [[10,30],[30,40]],[5,5], kal_dat, Speicherort = "testneu.txt", para = "")
#Kalibrierung([["Emax"]], [[40,41]],[2], kal_dat, Bedingung = True, Speicherort = "test.txt", para = para)



Kalibrierung([["Emax"],["Kontaktmaterialdicke"]], [[35,45],[10,40]],[5,5], kal_dat, Speicherort = "testneu.txt", para = para)
#Kalibrierung([["charzucont"],["Emax"]], [[0.8,1.1],[34,45]],[4,4], kal_dat, Speicherort = "testneu1.txt", para = para)
