import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.Detektor import Detektor
import matplotlib.pyplot as plt
from numba import jit



class Calc_I():
    def __init__(self,
                 Dateipfad='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT',
                 Element_Probe="Rh", Röhrenmaterial="Rh", Einfallswinkelalpha=20, Einfallswinkelbeta=70,
                 Fensterwinkel=0,
                 Fenstermaterial_röhre="Be", Fensterdicke_röhre=125, Raumwinkel=1, Röhrenstrom=0.01, Emin=0, Emax=35,
                 step=0.05, Messzeit=30, charzucont = 1,
                 Fenstermaterial_det="Be", Fensterdicke_det=7.62, phi_det=0, Kontaktmaterial="Au",
                 Kontaktmaterialdicke=50, Bedeckungsfaktor=1,
                 Detektormaterial="Si", Totschicht=0.05, activeLayer=3):
        self.Detektor = Detektor(Fenstermaterial=Fenstermaterial_det, Fensterdicke=Fensterdicke_det, phi=phi_det,
                                 Kontakmaterial=Kontaktmaterial, Kontaktmaterialdicke=Kontaktmaterialdicke,
                                 Bedeckungsfaktor=Bedeckungsfaktor, Detektormaterial=Detektormaterial,
                                 Totschicht=Totschicht, activeLayer=activeLayer,
                                 Dateipfad=Dateipfad, Emin=Emin, Emax=Emax, step=step)
        self.Röhre = Röhre(Röhrenmaterial=Röhrenmaterial, Einfallswinkelalpha=Einfallswinkelalpha,
                           Einfallswinkelbeta=Einfallswinkelbeta, Fensterwinkel=Fensterwinkel,
                           Fenstermaterial=Fenstermaterial_röhre, Fensterdicke=Fensterdicke_röhre,
                           Raumwinkel=Raumwinkel, Röhrenstrom=Röhrenstrom, Emin=Emin, Emax=Emax,
                           step=step, Messzeit=Messzeit, folder_path=Dateipfad, charzucont=charzucont)
        self.Dateipfad = Dateipfad
        self.Element_Probe = Element_Probe
        self.Emin = Emin if Emin != 0 else step
        self.Emax = Emax
        self.step = step

        #self.Element = Element(Dateipfad=Dateipfad, Element=Element_Probe, Emin = Emin, Emax = Emax, step = step)
    def Geometriefaktor_ati_K(self, Tupel):   #(Element, Intensität)
        x_Element = Element(Dateipfad=self.Dateipfad, Element=Tupel[0], Emin = self.Emin, Emax = self.Emax, step = self.step)
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        #const = 0.135047447423566
        counts_K = 0
        for j in x_Element.Ubergange():
            if (j[0][1] == "K" and j[0][3] == "L"):
                if (j[0][0:2] ==" K" ):
                    Energie = x_Element.Kanten()[0][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] == "L1" ):
                    Energie = x_Element.Kanten()[1][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] == "L2" ):
                    Energie = x_Element.Kanten()[2][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] =="L3"):
                    Energie = x_Element.Kanten()[3][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)

                for k in range(int(Energie/self.step),len(x_Element.tau[0])):
                    dummy += self.Röhre.Countrate_gesamt[1][k] * x_Element.tau[1][k] * x_Element.S_ij(j[0][0:2], x_Element.tau[0][k]) * x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.mü[1][k]/cos + x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)

                    #counts += dummy * Det.Detektoreffizienz(j[1]) * const
                if (j[0][0:2] ==" K" and j[0][3:4] == "L"):
                    counts_K += dummy * self.Detektor.Detektoreffizienz(j[1]) * const
                    print("primcount", dummy * self.Detektor.Detektoreffizienz(j[1]) * const, "Übergang", j[0])
        #print(x_Element.Get_Elementsymbol(),Tupel[1] / counts_K)
        print("gesamt", counts_K)
        return (Tupel[1] / counts_K, x_Element.K_gemittel_ubergang(),x_Element.Get_Elementsymbol())

    def Geometriefaktor_ati_L(self, Tupel):   #(Element, Intensität)
        x_Element = Element(Dateipfad=self.Dateipfad, Element=Tupel[0], Emin = self.Emin, Emax = self.Emax, step = self.step)
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        #const = 0.135047447423566
        counts_K = 0
        print(x_Element.Ubergange())
        for j in x_Element.Ubergange():
            if (j[0][0:2] == "L3" and (j[0][3:5] == "M4" or j[0][3:5] == "M5")):
                if (j[0][0:2] ==" K" ):
                    Energie = x_Element.Kanten()[0][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] == "L1" ):
                    Energie = x_Element.Kanten()[1][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] == "L2" ):
                    Energie = x_Element.Kanten()[2][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)
                if (j[0][0:2] =="L3"):
                    Energie = x_Element.Kanten()[3][1]
                    step = (int(Energie/self.step)+1)*self.step - Energie
                    dummy = (self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]) * x_Element.Massenabsorptionskoeffizient(Energie)[1][0]*(x_Element.S_ij(j[0][0:2], Energie))*x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.Massenschwächungskoeffizient(Energie)[1][0]/cos+x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)

                for k in range(int(Energie/self.step),len(x_Element.tau[0])):
                    dummy += self.Röhre.Countrate_gesamt[1][k] * x_Element.tau[1][k] * x_Element.S_ij(j[0][0:2], x_Element.tau[0][k]) * x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.mü[1][k]/cos + x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)

                    #counts += dummy * Det.Detektoreffizienz(j[1]) * const
                #if (j[0][0:2] ==" K" and j[0][3:4] == "L"):
                counts_K += dummy * self.Detektor.Detektoreffizienz(j[1]) * const
                print("primcount", dummy * self.Detektor.Detektoreffizienz(j[1]) * const, "Übergang", j[0])
        #print(x_Element.Get_Elementsymbol(),Tupel[1] / counts_K)
        print("gesamt", counts_K)
        return (Tupel[1] / counts_K, x_Element.K_gemittel_ubergang(),x_Element.Get_Elementsymbol())


    def Sekundäranregung(self, tupel):   #(Element, Intensität)
        x_Element = Element(Dateipfad=self.Dateipfad, Element=tupel[0], Emin = self.Emin, Emax = self.Emax, step = self.step)
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2


        for i in x_Element.Ubergange():
            print(i[0])
            countrate = 0
            for a in x_Element.Kanten():
                if (i[0][0:2] == a[0]):
                    Kante = a[1]
            for j in x_Element.Ubergange():
                if (Kante < j[1]):
                    for b in x_Element.Kanten():
                        if (j[0][0:2] == b[0]):
                            Kante_xyz = b[1]
                    #print("angeret durch", j[0])
                    myc_b = x_Element.Massenschwächungskoeffizient(Kante_xyz)[1][0]
                    myc_ijk = x_Element.Massenschwächungskoeffizient(i[1])[1][0]
                    myc_abc = x_Element.Massenschwächungskoeffizient(j[1])[1][0]
                    integral = cos / myc_ijk * np.log(1 + myc_ijk / (cos * myc_abc))
                    #print(integral)
                    integral += (cos / myc_b) * np.log(1 + myc_b / (cos * myc_abc))
                    #print(integral)
                    #integral *=

                    step = (int(Kante_xyz/self.step)+1)*self.step - Kante_xyz
                    #print("tube", (self.Röhre.GetCountRateChar(Kante_xyz, step)+self.Röhre.GetCountRateCont(Kante_xyz, step)[0][0]))
                    #print("M_j", x_Element.S_ij(j[0][0:2], Kante_xyz))
                    #x_Element.Omega_Schale(j[0][0:2])*j[2]
                    #print("wp_jk",)
                    tube_b = self.Röhre.GetCountRateChar(Kante_xyz, step) + self.Röhre.GetCountRateCont(Kante_xyz, step)[0][0]
                    integral *= x_Element.S_ij(j[0][0:2], Kante_xyz) * tube_b * x_Element.Omega_Schale(j[0][0:2])*j[2]*x_Element.Massenabsorptionskoeffizient(Kante_xyz)[1][0] / ((myc_b / cos)+(myc_ijk/cos))
                    #print(integral)
                    integralconst = cos / myc_ijk * np.log(1 + myc_ijk / (cos * myc_abc))
                    for k in range(int(Kante_xyz/self.step), len(x_Element.tau[0])):
                        dummy = integralconst + (cos / x_Element.mü[1][k] * np.log(1 + x_Element.mü[1][k] / (cos * myc_abc)))
                        dummy *= x_Element.S_ij(j[0][0:2], x_Element.tau[0][k]) * x_Element.Omega_Schale(j[0][0:2])*j[2] * self.Röhre.Countrate_gesamt[1][k] * x_Element.tau[1][k] / (x_Element.mü[1][k] / cos + myc_ijk / cos)
                        integral += dummy
                    #print(integral, j[0])
                    integral *= const * x_Element.S_ij(i[0][0:2], j[1]) * x_Element.Omega_Schale(i[0][0:2])*i[2] * self.Detektor.Detektoreffizienz(i[1]) * 0.5 * x_Element.Massenabsorptionskoeffizient(j[1])[1][0]
                    #print("const",const, "Mj",x_Element.S_ij(i[0][0:2], j[1]), "wpjk", x_Element.Omega_Schale(i[0][0:2])*i[2], "det", self.Detektor.Detektoreffizienz(i[1]), "tau", x_Element.Massenabsorptionskoeffizient(j[1])[1][0])
                    countrate += integral
                    #print(integral, j[0])
            print(countrate)







#Cal = Calc_I(Röhrenstrom=0.01, Messzeit = 30, Emax = 40, Fensterdicke_det=12)
#print("ag",Cal.Geometriefaktor_ati(("ag",56092)))
#print("cd",Cal.Geometriefaktor_ati(("cd",45135)))
#print("sn",Cal.Geometriefaktor_ati(("sn",24885)))

#Cal1 = Calc_I(Röhrenstrom=0.01, Messzeit = 30, Emax = 35, Fensterdicke_det=12)
#print(Cal1.Geometriefaktor_ati(("ag",24886)))
