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
y_data_scipy=[]
y_data_boby=[]
y_data_lm=[]
y_data_lm_scipy=[]

for kal in kal_dat:
    x_ele=Element(Element=kal[0])
    if kal[2]==0:
        x_data.append(x_ele.K_gemittel_ubergang())
    else:
        x_data.append(x_ele.L_gemittel_ubergang())


for kal in kal_dat:
    Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=15, activeLayer=2.06872613, Totschicht=8.54277948e-04, charzucont_L=2.02373175e-01,
                charzucont=8.12735451e-01,Emax=4.49994894e+01,Kontaktmaterialdicke=3.98246503e+01)
    print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
    y_data_scipy.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))



#for kal in kal_dat:
 #   Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=15, activeLayer=2.993489938788493, Totschicht=0.0, charzucont_L=1.1997371366790963,
 #               charzucont=0.949251062884446,Emax=44.87403458252088,Kontaktmaterialdicke=10.0)
#    print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
#    y_data_boby.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))

#for kal in kal_dat:
  #  Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=15, activeLayer= 2.9229864656423263, Totschicht=0.0, charzucont_L=1.2,
  #              charzucont=0.95,Emax=45,Kontaktmaterialdicke=14.442617636447068)
 #   print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
 #   y_data_lm.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))

for kal in kal_dat:
    Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=-30.48201104, activeLayer= 2.81941896, Totschicht=0.5695597, charzucont_L=-2.67399482,
                charzucont=1.09349746,Emax=45.66091736,Kontaktmaterialdicke=-9.49609831)
    print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
    y_data_lm_scipy.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))


#for kal in kal_dat:
 #   Ki = Calc_I(Konzentration=[1], P1=[kal[0]], Übergänge=[kal[2]], Einfallswinkelalpha=4.666493320690118, activeLayer= 1.5491262717716114, Totschicht=-5.666609973797417, charzucont_L=1.2,
 #               charzucont=0.95,Emax=49.47407058487551,Kontaktmaterialdicke=125.8230963435906)
 #   print(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
 #   y_data_lm2.append(kal[1]/(Ki.Intensität_alle_jit_fürMinimierung([1])[0][0]))







for i in range(3):

   # Plot_einfach([x_data,y_data_lm,elemente], xy_format=True).plot_scatter(ylabel="lm",abweichung=True)
   # plt.show()


   # Plot_einfach([x_data,y_data_boby,elemente], xy_format=True).plot_scatter(ylabel="boby",abweichung=True)
   # plt.show()


    Plot_einfach([x_data,y_data_scipy,elemente], xy_format=True).plot_scatter(ylabel="Scipy",abweichung=True)
    plt.show()

    Plot_einfach([x_data,y_data_lm_scipy,elemente], xy_format=True).plot_scatter(ylabel="Scipy_lm",abweichung=True)
    plt.show()








#Scipy
#[1.50000000e+01 2.06872613e+00 8.54277948e-04 2.02373175e-01
 #8.12735451e-01 4.49994894e+01 3.98246503e+01]

"""
Startwerte=[15,3,0,1.2,0.95,45,10]

Optimierte Parameter (BOBYQA):
Einfallswinkelalpha = 15.0
activeLayer = 2.993489938788493
Totschicht = 0.0
charzucont_L = 1.1997371366790963
charzucont = 0.949251062884446
Emax = 44.87403458252088
Kontaktmaterialdicke = 10.0



Optimierte Parameter (LM):
Einfallswinkelalpha = 15.0
activeLayer = 2.9229864656423263
Totschicht = 0.0
charzucont_L = 1.2
charzucont = 0.95
Emax = 45.0
Kontaktmaterialdicke = 14.442617636447068

"""
