from Nachbau_ati_sauber.Element import Element
import numpy as np
from Nachbau_ati_sauber.Calc_I import Calc_I#ohne al, si
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
import matplotlib.pyplot as plt

Elemente = [(140000, 'Ag'), (66746, 'SN'), (163000, 'TI'), (111267, 'CD'), (433090, 'CU'), (196370, 'V'), (544606, 'ZR')
, (464025, 'ZN'), (498315, 'GE'), (10844, 'AL'), (20692, 'SI'), (106785, 'BI'), (13396, 'CD'), (17196, 'SN'), (109041, 'PB'), (82738, 'TA'),(13240, 'Ag')]

Übergänge = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


kal_dat = []

for index, i in enumerate(Elemente):
    kal_dat.append([i[1], i[0], Übergänge[index]])
print(kal_dat)

elemente = [entry[0] for entry in kal_dat]
intensität = [entry[1] for entry in kal_dat]
print(elemente,Übergänge)

x_data=[]
y_data=[]


for kal in kal_dat:
    x_ele=Element(Element=kal[0])
    if kal[2]==0:
        x_data.append(x_ele.K_gemittel_ubergang())
    else:
        x_data.append(x_ele.L_gemittel_ubergang())


for kal in kal_dat:
    Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=15, activeLayer= 2.9229864656423263, Totschicht=0.0, charzucont_L=1.2,
                charzucont=0.95,Emax=45,Kontaktmaterialdicke=14.442617636447068,Fensterdicke_röhre=500)
    print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
    y_data.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))

print("noch ok")
Plot_einfach([x_data,y_data,elemente], xy_format=True).plot_scatter(ylabel="lm",abweichung=True)
plt.show()





#Scipy
