import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.Detektor import Detektor
import matplotlib.pyplot as plt
from numba import njit
from scipy.optimize import least_squares
from Nachbau_ati_sauber.packages.Funktionen_Calc_I import *
from Nachbau_ati_sauber.packages.Funktionen import *

class Calc_I():
    def __init__(self,
                 Dateipfad='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT',
                 Element_Probe="Ag", Röhrenmaterial="Rh", Einfallswinkelalpha=20, Einfallswinkelbeta=70,
                 Fensterwinkel=0, sigma = 1.0314, charzucont_L = 1,
                 Fenstermaterial_röhre="Be", Fensterdicke_röhre=125, Raumwinkel=1, Röhrenstrom=0.01, Emin=0, Emax=35,
                 step=0.05, Messzeit=30, charzucont = 1, Übergänge = "alle_K",
                 Fenstermaterial_det="Be", Fensterdicke_det=7.62, phi_det=0, Kontaktmaterial="Au",
                 Kontaktmaterialdicke=50, Bedeckungsfaktor=1, P1=[], Palpha =45, Pbeta = 45,
                 Detektormaterial="Si", Totschicht=0.05, activeLayer=3, Konzentration = [1], dark_M = 11):
        self.Detektor = Detektor(Fenstermaterial=Fenstermaterial_det, Fensterdicke=Fensterdicke_det, phi=phi_det,
                                 Kontakmaterial=Kontaktmaterial, Kontaktmaterialdicke=Kontaktmaterialdicke,
                                 Bedeckungsfaktor=Bedeckungsfaktor, Detektormaterial=Detektormaterial,
                                 Totschicht=Totschicht, activeLayer=activeLayer,
                                 Dateipfad=Dateipfad, Emin=Emin, Emax=Emax, step=step)
        self.Röhre = Röhre(Röhrenmaterial=Röhrenmaterial, Einfallswinkelalpha=Einfallswinkelalpha,
                           Einfallswinkelbeta=Einfallswinkelbeta, Fensterwinkel=Fensterwinkel, sigma=sigma,
                           Fenstermaterial=Fenstermaterial_röhre, Fensterdicke=Fensterdicke_röhre,
                           Raumwinkel=Raumwinkel, Röhrenstrom=Röhrenstrom, Emin=Emin, Emax=Emax,
                           step=step, Messzeit=Messzeit, folder_path=Dateipfad, charzucont=charzucont,
                           charzucont_L=charzucont_L)
        self.Fensterdicke_det=Fensterdicke_det * 1e-4
        self.Dateipfad = Dateipfad
        self.Element_Probe = Element_Probe
        self.Palpha = np.cos(np.pi / 180 * Palpha)
        self.Pbeta = np.cos(np.pi / 180 * Pbeta)
        self.Emin = Emin if Emin != 0 else step
        self.Emax = Emax
        self.step = step
        self.Konzentration = np.array(Konzentration)
        self.Probe1 = [int(Element(Element=i, Dateipfad=Dateipfad).Get_Atomicnumber()) for i in P1]
        #self.Probe1 = P1
        self.Übergänge = self.Übergänge_eingabe(Übergänge)
        self.dark_M = dark_M

    def Übergänge_eingabe(self, Übergänge):
        """
        Überprüft, ob die Übergänge "alle_K" sein sollen, und setzt den Wert entsprechend.
        """
        if Übergänge == "alle_K":
            # Falls "alle_K", gib ein Array mit Nullen zurück (angepasst an die Länge von Konzentration)
            return np.zeros(len(self.Konzentration))
        else:
            # Andernfalls konvertiere Übergänge in ein NumPy-Array (falls es eine Liste ist)
            return np.array(Übergänge)


    def Werte_vorbereiten_alle_jit(self):
        Probe = Probeneingabe(self.Probe1)
        Elementliste = []
        alle_Kanten = []
        mau = 0 #maximale Anzahl Übergänge
        Tau, Mü, Ltf = [],[],[]
        for i in Probe: #i=Element
            erstellte_Element = Element(Dateipfad=self.Dateipfad, Element=i, Emin = self.Emin, Emax = self.Emax, step = self.step)
            Elementliste.append(erstellte_Element)
            alle_Kanten.append([Kante[1] for Kante in erstellte_Element.Kanten()[0:4]])
            mau = max(mau, len(erstellte_Element.Ubergange()))
            Tau.append(erstellte_Element.tau[1])
            Mü.append(erstellte_Element.mü[1])
            Ltf.append(erstellte_Element.Löcherübertrag())
        alle_Übergänge = np.zeros((len(Elementliste), mau, 3))
        for index, x_Element in enumerate(Elementliste):
            if x_Element.Ubergange() == [[]]:
                pass
            else:
                for index_über, Über in enumerate(x_Element.Ubergange()):
                    alle_Übergänge[index][index_über] = [str_zu_zahl(Über[0]), Über[1], Über[2]]
        Tube0, Tau0, Omega0, Sij0 = (np.zeros((len(Elementliste), 4)) for _ in range(4))
        Sij = np.zeros((len(Elementliste), 4, len(Tau[0])))
        Det_ijk = np.zeros((len(Elementliste), mau))
        for index, x_Element in enumerate(Elementliste):
            for Kantenindex, Energie in enumerate(alle_Kanten[index]):
                step = (int(Energie/self.step)+1)*self.step - Energie
                if (Energie==0):
                    Energie=0.000001
                Tube0[index][Kantenindex] = self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]
                Tau0[index][Kantenindex] = x_Element.Massenabsorptionskoeffizient(Energie)[1][0]
                Sij0[index][Kantenindex] = x_Element.S_ij(x_Element.Kanten()[Kantenindex][0], Energie)
                Omega0[index][Kantenindex] = x_Element.Omega_Schale(x_Element.Kanten()[Kantenindex][0])
                Sij[index][Kantenindex] = [x_Element.S_ij(x_Element.Kanten()[Kantenindex][0][0:2], (k + int(self.Emin/self.step)) * self.step) for k in range(len(Tau[0]))]
        index = 0
        Mü0 = np.zeros(len(Elementliste) * len(np.array(alle_Kanten).flatten()))
        for x_ele in Elementliste:
            for Energie in np.array(alle_Kanten).flatten():
                if Energie != 0:
                    Mü0[index] = x_ele.Massenschwächungskoeffizient(Energie)[1][0]
                    index += 1
                else:
                    index += 1
        Mü0 = np.reshape(Mü0, (len(Elementliste),  len(Elementliste), 4))
        alle_Übergangsenergien = []
        for i, Übergänge in enumerate(alle_Übergänge):
            for j, Übergang in enumerate(Übergänge):
                if (Übergang[1] != 0):
                    Det_ijk[i][j] = self.Detektor.Detektoreffizienz(Übergang[1])
                    alle_Übergangsenergien.append(Übergang[1])
                else:
                    alle_Übergangsenergien.append(0)
        index = 0
        Tau_ijk, Mü_ijk = (np.zeros(len(Elementliste) * len(alle_Übergangsenergien)) for _ in range(2))
        for x_ele in Elementliste:
            for Energie in alle_Übergangsenergien:
                if (Energie != 0):
                    Tau_ijk[index] = x_ele.Massenabsorptionskoeffizient(Energie)[1][0]
                    Mü_ijk[index] = x_ele.Massenschwächungskoeffizient(Energie)[1][0]
                    index += 1
                else:
                    index += 1
        Tau_ijk = np.reshape(Tau_ijk, (len(Elementliste),  int(len(alle_Übergangsenergien)/mau), mau))
        Mü_ijk = np.reshape(Mü_ijk, (len(Elementliste),  int(len(alle_Übergangsenergien)/mau), mau))
        Countrate = self.Röhre.Countrate_gesamt[1]
        Sij_xyz = np.zeros(len(Elementliste) * 4 * len(alle_Übergangsenergien))
        index = 0
        for x_Ele in Elementliste:
            for Kante in [" K", "L1", "L2", "L3"]:
                for Energie in alle_Übergangsenergien:
                    Sij_xyz[index] = x_Ele.S_ij(Kante, Energie)
                    index += 1
        Sij_xyz = np.reshape(Sij_xyz, (len(Elementliste), 4, len(alle_Übergangsenergien)))
        try:
            Konzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        except:
            print("keine Konzentrationen eingegeben")
        return self.Palpha, self.Pbeta, np.array(Tube0), np.array(Tau0), np.array(Omega0), np.array(Mü0), np.array(Sij0), np.array(Tau), np.array(Mü), np.array(Countrate), np.array(Mü_ijk), np.array(Det_ijk), np.array(Sij), np.array(alle_Kanten), np.array(alle_Übergänge), np.array(Sij_xyz), np.array(Tau_ijk), np.array(Konzentration), self.step, self.Emin, np.array(Ltf)


    def Werte_vorbereiten_Sekundär(self,Sekundärtarget, Einfallswinkelalpha_sek, Einfallswinkelbeta_sek):
        try:
            Probe, Konzentration = Verbindung_einlesen(Sekundärtarget)
            Konzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        except:
            print("Sekundärtarget falsch")
        Probe = Probeneingabe(Probe)
        #print(Probe)
        Elementliste = []
        alle_Kanten = []
        mau = 0 #maximale Anzahl Übergänge
        Tau, Mü, Ltf = [],[],[]
        for i in Probe: #i=Element
            erstellte_Element = Element(Dateipfad=self.Dateipfad, Element=i, Emin = self.Emin, Emax = self.Emax, step = self.step)
            Elementliste.append(erstellte_Element)
            alle_Kanten.append([Kante[1] for Kante in erstellte_Element.Kanten()[0:4]])
            mau = max(mau, len(erstellte_Element.Ubergange()))
            Tau.append(erstellte_Element.tau[1])
            Mü.append(erstellte_Element.mü[1])
            Ltf.append(erstellte_Element.Löcherübertrag())
        alle_Übergänge = np.zeros((len(Elementliste), mau, 3))
        for index, x_Element in enumerate(Elementliste):
            if x_Element.Ubergange() == [[]]:
                pass
            else:
                for index_über, Über in enumerate(x_Element.Ubergange()):
                    alle_Übergänge[index][index_über] = [str_zu_zahl(Über[0]), Über[1], Über[2]]
        Tube0, Tau0, Omega0, Sij0 = (np.zeros((len(Elementliste), 4)) for _ in range(4))
        Sij = np.zeros((len(Elementliste), 4, len(Tau[0])))
        Det_ijk = np.zeros((len(Elementliste), mau))
        for index, x_Element in enumerate(Elementliste):
            for Kantenindex, Energie in enumerate(alle_Kanten[index]):
                step = (int(Energie/self.step)+1)*self.step - Energie
                if (Energie==0):
                    Energie=0.000001
                Tube0[index][Kantenindex] = self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0]
                Tau0[index][Kantenindex] = x_Element.Massenabsorptionskoeffizient(Energie)[1][0]
                Sij0[index][Kantenindex] = x_Element.S_ij(x_Element.Kanten()[Kantenindex][0], Energie)
                Omega0[index][Kantenindex] = x_Element.Omega_Schale(x_Element.Kanten()[Kantenindex][0])
                Sij[index][Kantenindex] = [x_Element.S_ij(x_Element.Kanten()[Kantenindex][0][0:2], (k + int(self.Emin/self.step)) * self.step) for k in range(len(Tau[0]))]
        index = 0
        Mü0 = np.zeros(len(Elementliste) * len(np.array(alle_Kanten).flatten()))
        for x_ele in Elementliste:
            for Energie in np.array(alle_Kanten).flatten():
                if Energie != 0:
                    Mü0[index] = x_ele.Massenschwächungskoeffizient(Energie)[1][0]
                    index += 1
                else:
                    index += 1
        Mü0 = np.reshape(Mü0, (len(Elementliste),  len(Elementliste), 4))
        alle_Übergangsenergien = []
        for i, Übergänge in enumerate(alle_Übergänge):
            for j, Übergang in enumerate(Übergänge):
                if (Übergang[1] != 0):
                    Det_ijk[i][j] = 1       #gibt keinen Det bei Sekundär
                    alle_Übergangsenergien.append(Übergang[1])
                else:
                    alle_Übergangsenergien.append(0)
        index = 0
        Tau_ijk, Mü_ijk = (np.zeros(len(Elementliste) * len(alle_Übergangsenergien)) for _ in range(2))
        for x_ele in Elementliste:
            for Energie in alle_Übergangsenergien:
                if (Energie != 0):
                    Tau_ijk[index] = x_ele.Massenabsorptionskoeffizient(Energie)[1][0]
                    Mü_ijk[index] = x_ele.Massenschwächungskoeffizient(Energie)[1][0]
                    index += 1
                else:
                    index += 1
        Tau_ijk = np.reshape(Tau_ijk, (len(Elementliste),  int(len(alle_Übergangsenergien)/mau), mau))
        Mü_ijk = np.reshape(Mü_ijk, (len(Elementliste),  int(len(alle_Übergangsenergien)/mau), mau))
        Countrate = self.Röhre.Countrate_gesamt[1]
        Sij_xyz = np.zeros(len(Elementliste) * 4 * len(alle_Übergangsenergien))
        index = 0
        for x_Ele in Elementliste:
            for Kante in [" K", "L1", "L2", "L3"]:
                for Energie in alle_Übergangsenergien:
                    Sij_xyz[index] = x_Ele.S_ij(Kante, Energie)
                    index += 1
        Sij_xyz = np.reshape(Sij_xyz, (len(Elementliste), 4, len(alle_Übergangsenergien)))
        return np.cos(Einfallswinkelalpha_sek*np.pi/180), np.cos(Einfallswinkelbeta_sek*np.pi/180), np.array(Tube0), np.array(Tau0), np.array(Omega0), np.array(Mü0), np.array(Sij0), np.array(Tau), np.array(Mü), np.array(Countrate), np.array(Mü_ijk), np.array(Det_ijk), np.array(Sij), np.array(alle_Kanten), np.array(alle_Übergänge), np.array(Sij_xyz), np.array(Tau_ijk), np.array(Konzentration), self.step, self.Emin, np.array(Ltf)


    def Intensität_alle_jit(self):
        Geo = 2.4e-05
        Werte = self.Werte_vorbereiten_alle_jit()
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        L_übergänge = ["L3-M4", "L3-M5"]

        element = 0
        counts_array = []
        x_Ele = Element(Element=self.Probe1[element], Dateipfad=self.Dateipfad)
        #print(x_Ele.Get_Elementsymbol())
        for ele in range(len(Prim)):
            counts = 0
            #x_Ele = Element(Element = self.Probe1[ele])
            for index, i in enumerate(Prim[ele]):
                if Sek[ele][index][0] != 0:
                    if(self.Übergänge[ele] == 0):
                        if (zahl_zu_string(i[0]) in K_übergänge):
                            counts += add[ele][index][1]
                    else:
                        if (zahl_zu_string(i[0]) in L_übergänge):
                            counts += add[ele][index][1]
            if (counts == 0):
                counts = 1
            #print(x_Ele.Get_Elementsymbol(), counts * Geo)
            counts_array.append(counts)
        #return counts_array
        Iterationen = 1
        ##print(self.Konzentration)
        while (Iterationen < 10):
            Iterationen += 1
            ##print("iteration",Iterationen)
            Werte = list(Werte)  # Tuple in Liste umwandeln
            if ( Iterationen ==2):
                ##print(Werte[-3])
                #erste_Konzentartion = Werte[-3]
                pass
            #print(counts_array)
            #print(self.Konzentration)
            Werte[-4] *= self.Konzentration/np.array(counts_array)/Geo
            #Werte[-3] *= erste_Konzentartion/np.array(counts_array)/Geo
            ##print("summe Konzentration",Werte[-3][0]+Werte[-3][1])
            ###print(("konzentration",Werte[-3]))
            retval = Werte[-4]
            ###print("gemittelt",Werte[-3]/(Werte[-3][0]+Werte[-3][1]))
            Werte = tuple(Werte)
            Prim = Primärintensität_berechnen_alle_jit(*Werte)
            Sek = Sekundärintensität_berechnen_jit(*Werte)
            add = Prim.copy()
            add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
            counts_array = []

            for ele in range(len(Prim)):
                counts = 0
                #x_Ele = Element(Element = self.Probe1[ele])
                for index, i in enumerate(Prim[ele]):
                    if Sek[ele][index][0] != 0:
                        if(self.Übergänge[ele] == 0):
                            if (zahl_zu_string(i[0]) in K_übergänge):
                                counts += add[ele][index][1]
                        else:
                            if (zahl_zu_string(i[0]) in L_übergänge):
                                counts += add[ele][index][1]
                if (counts == 0):
                    counts = 1
                #print(x_Ele.Get_Elementsymbol(), counts * Geo)
                counts_array.append(counts)

            #print(np.array(counts_array)*Geo)
            ##print(self.Konzentration/Geo)
        ###print("alleCounts",np.array(counts_array)*Geo)
        ###print("relativer Unterschied",np.array(counts_array)*Geo/self.Konzentration)
        ###print("Differenz",np.array(counts_array)*Geo-self.Konzentration)
            ##print([self.Konzentration[i]/Geo/counts_array[i] for i in range(len(counts_array))])
            #Werte = Werte[:-3] + self.Konzentration/np.array(counts_array) + Werte[-2:]
        #return np.array(counts)
        #return retval
            values = np.array(([i/retval.sum()*100 for i in retval]))
            ######print(" & ".join([f"{value:.2f}" for value in values]) + " \\\\")
        return [i/retval.sum()*100 for i in retval]


    def Intensität_Sekundärtarget(self, Sekundärtarget, Konzentration, Einfallswinkelalpha_sek = 45, Einfallswinkelbeta_sek = 45):#noch filter hinzufügen, eigener Geometriefaktor?
        Werte = self.Werte_vorbereiten_Sekundär(Sekundärtarget, Einfallswinkelalpha_sek, Einfallswinkelbeta_sek)
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        Werte = self.Werte_vorbereiten_alle_jit()
        Werte = list(Werte)
        Werte[2][:] = 0     #I0 an der Kante
        Werte[9][:] = 0     #I allgemein
        for i in range(len(add)):
            for j in range(len(add[i])):
                if (add[i][j][1] >= 1 and add[i][j][2] > self.Emin):
                    Energie = int(add[i][j][2] / self.step - self.Emin / self.step + 1)
                    Werte[9][Energie] += add[i][j][1]
        Anregspek = Werte[9]
        Werte[-4] = Konzentration
        Werte = tuple(Werte)
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        L_übergänge = ["L3-M4", "L3-M5"]
        counts_array = []
        for ele in range(len(Prim)):
            counts = 0
            for index, i in enumerate(Prim[ele]):
                if Sek[ele][index][0] != 0:
                    if(self.Übergänge[ele] == 0):
                        if (zahl_zu_string(i[0]) in K_übergänge):
                            counts += add[ele][index][1]
                    else:
                        if (zahl_zu_string(i[0]) in L_übergänge):
                            counts += add[ele][index][1]
           # if (counts == 0):
            #    counts = 1
            counts_array.append(counts)
        return np.array(counts_array), add, Anregspek


        #for k in range(int(alle_Kanten[j][Kante_xy] / step + Emin / step - 1), len(Tau[j])):

        return add

    def Intensität_monoenergetisch(self, Konzentration, Energie):
        Werte = self.Werte_vorbereiten_alle_jit()
        Werte = list(Werte)  # Tuple in Liste umwandeln
        Werte[-4] = Konzentration
        Werte[2][:] = 0     #I0 an der Kante
        Werte[9][:] = 0     #I allgemein
        Energie = int(Energie / self.step - self.Emin / self.step + 1)
        #Werte[9][Energie] += 1000000
        Werte[9][Energie] += 3*10**10

        Werte = tuple(Werte)
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        L_übergänge = ["L3-M4", "L3-M5"]
        element = 0
        counts_array = []
        #x_Ele = Element(Element = self.Probe1[element])
        for ele in range(len(Prim)):
            counts = 0
            #x_Ele = Element(Element = self.Probe1[ele])
            for index, i in enumerate(Prim[ele]):
                if Sek[ele][index][0] != 0:
                    if(self.Übergänge[ele] == 0):
                        if (zahl_zu_string(i[0]) in K_übergänge):
                            counts += add[ele][index][1]
                    else:
                        if (zahl_zu_string(i[0]) in L_übergänge):
                            counts += add[ele][index][1]

           # if (counts == 0):
            #    counts = 1
            counts_array.append(counts)
        return np.array(counts_array), add


    #Funktion zu löschen
    def Intensität_K_alle_jit_fürSekundärtarget(self, Sekundärtarget, Konzentration):   #einfach ohne Detektoreffizienz
        safe = self.Probe1
        self.Probe1 = Sekundärtarget
        #print("ausMin",self.Probe1)
        Werte = self.Werte_vorbereiten_alle_jit()
        self.Probe1 = safe
        Werte = list(Werte)  # Tuple in Liste umwandeln
        Werte[-4] = Konzentration
        Werte = tuple(Werte)
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        #print(add)
        x = add
        for i in range(len(x[:,:,0])):
            for index, j in enumerate(x[:,:,0][i]):
                #pass
                if x[:,:,2][i][index] !=0:
                    #print(self.Detektor.Detektoreffizienz(x[:,:,2][i][index]), x[:,:,2][i][index],x[:,:,1][i][index])
                    x[:,:,1][i][index] = x[:,:,1][i][index] / self.Detektor.Detektoreffizienz(x[:,:,2][i][index])
        return x


    def Intensität_alle_jit_fürMinimierung(self, Konzentration, vorbereitete_Werte=None):
        #Geo = 4 * 10**-7
        if vorbereitete_Werte is None:
            vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        #Werte = self.Werte_vorbereiten_alle_jit()
        #print(Werte)
        Werte = list(vorbereitete_Werte)  # Tuple in Liste umwandeln
        Werte[-4] = Konzentration
        Werte = tuple(Werte)
        Prim = Primärintensität_berechnen_alle_jit(*Werte)
        Sek = Sekundärintensität_berechnen_jit(*Werte)
        add = Prim.copy()
        add[:, :, 1] = Prim[:, :, 1] + Sek[:, :, 1]
        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        L_übergänge = ["L3-M4", "L3-M5"]
        element = 0
        counts_array = []
        #x_Ele = Element(Element = self.Probe1[element])
        for ele in range(len(Prim)):
            counts = 0
            #x_Ele = Element(Element = self.Probe1[ele])
            for index, i in enumerate(Prim[ele]):
                if Sek[ele][index][0] != 0:
                    if(self.Übergänge[ele] == 0):
                        if (zahl_zu_string(i[0]) in K_übergänge):
                            counts += add[ele][index][1]
                    else:
                        if (zahl_zu_string(i[0]) in L_übergänge):
                            counts += add[ele][index][1]

           # if (counts == 0):
            #    counts = 1
            counts_array.append(counts)
            #print(counts_array)
        return np.array(counts_array), add

    def Atiquant(self):
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        c = self.Konzentration/(self.Intensität_alle_jit_fürMinimierung(self.Konzentration,vorbereitete_Werte)[0])
        #print(self.Intensität_alle_jit_fürMinimierung(self.Konzentration,vorbereitete_Werte)[0])
        c = np.array([con / c.sum() for con in c])
        #print(c)
        for i in range(20):
            c *= self.Konzentration/(self.Intensität_alle_jit_fürMinimierung(c,vorbereitete_Werte)[0])
            c = np.array([con / c.sum() for con in c])
            #print("Konz",c)

        #print("INTENSITÄT",self.Intensität_alle_jit_fürMinimierung(c,vorbereitete_Werte)[0]*(self.Konzentration/self.Intensität_alle_jit_fürMinimierung(c,vorbereitete_Werte)[0])[0])




        return c, (self.Konzentration/self.Intensität_alle_jit_fürMinimierung(c,vorbereitete_Werte)[0])[0]


    def Minimierung_sqrt(self, Geo, Z_Gewichtung = 1, **kwargs):
        Startkonzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        gemessene_Intensitäten = self.Konzentration
        Z_gemittelt = kwargs.get('Z_gemittelt', None)
        def Residuen(Konzentration, gemessene_Intensitäten):
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration)[0] * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            if (Z_gemittelt != None):
                Konz_norm = np.array([con /Konzentration.sum() for con in Konzentration])
                Z_gem_be = sum(con * self.Probe1[index] for index, con in enumerate(Konz_norm))
                Z_gemittelt_array = np.full(len(Konzentration)-len(Auslassen), Z_gemittelt)
                Z_gem_be_array = np.full(len(Konzentration)-len(Auslassen), Z_gem_be)
                return np.abs((be_I - gem_I)/be_I**(1/2)) + np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array))

            return (be_I - gem_I)/be_I**(1/2)

        result = least_squares(
        Residuen,
        Startkonzentration,  # Startwerte für Konzentrationen
        args=( gemessene_Intensitäten,),bounds=(0, np.inf)  # Übergabe des Modells und der gemessenen Daten
        )
        # Optimierte Konzentrationen
        optimized_Konzentration = result.x

        Z_mittel_be = 0
        for index, con in enumerate(np.array([con / optimized_Konzentration.sum() for con in optimized_Konzentration])):
            Z_mittel_be += con * self.Probe1[index]
        if (Z_gemittelt != None):
            print("Mit Z_gemittelt",Z_gemittelt, "Gewichtung", Z_Gewichtung)
        else:
            print("ohne Z_gemittelt")
        ##print("Gemitteltes_Z", Z_mittel_be)
        ##print("Optimierte Konzentrationen NLLS:", optimized_Konzentration)
        print("Optimierte Konzentrationen NORMIERT NLLS in %:",np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration]))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        ##print("neues Residuum")
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + "{:.2e}".format(result.cost) + " & " + f"{Z_mittel_be:.2f}" + " \\\\")
        # Optional: Weitere Ergebnisse des least_squares-Verfahrens
        ##print("Kosten (Summe der quadrierten Residuen):", result.cost)
        #print("Erfolg:", result.success)
        #print("Nachricht:", result.message)
        print("Anzahl der Funktionsauswertungen:", result.nfev)
        #print("Jakobi:", result.jac)
        return optimized_Konzentration


    def Minimierung_sqrt_zusatz(self, Geo, Z_Gewichtung = 1, **kwargs):
        Startkonzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        gemessene_Intensitäten = self.Konzentration
        Z_gemittelt = kwargs.get('Z_gemittelt', None)
        def Residuen(Konzentration, gemessene_Intensitäten):
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration) * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            if (Z_gemittelt != None):
                Konz_norm = np.array([con /Konzentration.sum() for con in Konzentration])
                Z_gem_be = sum(con * self.Probe1[index] for index, con in enumerate(Konz_norm))
                Z_gemittelt_array = np.full(len(Konzentration)-len(Auslassen), Z_gemittelt)
                Z_gem_be_array = np.full(len(Konzentration)-len(Auslassen), Z_gem_be)
                return np.abs((be_I - gem_I)/be_I**(1/2)) + np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array) * be_I**(1/2))

            return (be_I - gem_I)/be_I**(1/2)

        result = least_squares(
        Residuen,
        Startkonzentration,  # Startwerte für Konzentrationen
        args=( gemessene_Intensitäten,),bounds=(0, np.inf)  # Übergabe des Modells und der gemessenen Daten
        )
        # Optimierte Konzentrationen
        optimized_Konzentration = result.x

        Z_mittel_be = 0
        for index, con in enumerate(np.array([con / optimized_Konzentration.sum() for con in optimized_Konzentration])):
            Z_mittel_be += con * self.Probe1[index]
        if (Z_gemittelt != None):
            print("Mit Z_gemittelt",Z_gemittelt, "Gewichtung", Z_Gewichtung)
        else:
            print("ohne Z_gemittelt")
        ##print("Gemitteltes_Z", Z_mittel_be)
        ##print("Optimierte Konzentrationen NLLS:", optimized_Konzentration)
        print("Optimierte Konzentrationen NORMIERT NLLS in %:",np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration]))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        ##print("neues Residuum")
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + "{:.2e}".format(result.cost) + " & " + f"{Z_mittel_be:.2f}" + " \\\\")
        # Optional: Weitere Ergebnisse des least_squares-Verfahrens
        ##print("Kosten (Summe der quadrierten Residuen):", result.cost)
        #print("Erfolg:", result.success)
        #print("Nachricht:", result.message)
        print("Anzahl der Funktionsauswertungen:", result.nfev)
        return optimized_Konzentration

    def Minimierung_relativ(self, Geo, Z_Gewichtung = 1, **kwargs):
        Startkonzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        gemessene_Intensitäten = self.Konzentration
        Z_gemittelt = kwargs.get('Z_gemittelt', None)

        def Residuen(Konzentration, gemessene_Intensitäten):
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration)[0] * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            if (Z_gemittelt != None):
                Konz_norm = np.array([con /Konzentration.sum() for con in Konzentration])
                Z_gem_be = sum(con * self.Probe1[index] for index, con in enumerate(Konz_norm))
                Z_gemittelt_array = np.full(len(Konzentration)-len(Auslassen), Z_gemittelt)
                Z_gem_be_array = np.full(len(Konzentration)-len(Auslassen), Z_gem_be)
                return np.abs((be_I - gem_I) / be_I) + np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array))

            return (be_I - gem_I) / be_I

        result = least_squares(
        Residuen,
        Startkonzentration,  # Startwerte für Konzentrationen
        args=( gemessene_Intensitäten,),bounds=(0, np.inf)  # Übergabe des Modells und der gemessenen Daten
        )
        # Optimierte Konzentrationen
        optimized_Konzentration = result.x

        Z_mittel_be = 0
        for index, con in enumerate(np.array([con / optimized_Konzentration.sum() for con in optimized_Konzentration])):
            Z_mittel_be += con * self.Probe1[index]
        if (Z_gemittelt != None):
            print("Mit Z_gemittelt",Z_gemittelt, "Gewichtung", Z_Gewichtung)
        else:
            print("ohne Z_gemittelt")
        ##print("Gemitteltes_Z", Z_mittel_be)
        ##print("Optimierte Konzentrationen NLLS:", optimized_Konzentration)
        print("Optimierte Konzentrationen NORMIERT NLLS in %:",np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration]))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        ##print("neues Residuum")
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + "{:.2e}".format(result.cost) + " & " + f"{Z_mittel_be:.2f}" + " \\\\")
        # Optional: Weitere Ergebnisse des least_squares-Verfahrens
        ##print("Kosten (Summe der quadrierten Residuen):", result.cost)
        #print("Erfolg:", result.success)
        #print("Nachricht:", result.message)
        print("Anzahl der Funktionsauswertungen:", result.nfev)
        return optimized_Konzentration

    def klasse_erstellen(self, einstellung):    #Übernahme für arrays, sprich Parameter, die ein Array als Input haben
        """
        Erstellt eine neue Instanz der Klasse mit denselben Parametern wie die aktuelle Instanz,
        aber mit den überschriebenen Werten aus `einstellung`.
        Berücksichtigt auch Werte aus `self.Detektor` und `self.Röhre`.
        """
        # Alle aktuellen Instanzwerte holen
        aktuelle_werte = vars(self).copy()

        # Werte aus self.Detektor extrahieren (falls vorhanden)
        if hasattr(self, "Detektor") and self.Detektor:
            aktuelle_werte.update(vars(self.Detektor))

        # Werte aus self.Röhre extrahieren (falls vorhanden)
        if hasattr(self, "Röhre") and self.Röhre:
            aktuelle_werte.update(vars(self.Röhre))

        # Falls `einstellung` ein Dictionary ist, kombiniere es mit den aktuellen Werten
        if not isinstance(einstellung, dict):
            raise TypeError("`einstellung` muss ein Dictionary sein.")

        updated_values = {**aktuelle_werte, **einstellung}  # Einstellung überschreibt aktuelle Werte

        # Die Parameter des Konstruktors holen
        signature = inspect.signature(self.__class__.__init__)
        erlaubte_argumente = set(signature.parameters.keys()) - {"self"}  # "self" entfernen

        # Nur erlaubte Parameter behalten

        gefilterte_values = {k: v for k, v in updated_values.items() if k in erlaubte_argumente}

        gefilterte_values["Palpha"] = np.arccos(gefilterte_values["Palpha"]) * 180 / np.pi
        gefilterte_values["Pbeta"] = np.arccos(gefilterte_values["Pbeta"]) * 180 / np.pi

        gefilterte_values["Fensterdicke_det"] /= 1e-4
        gefilterte_values["Kontaktmaterialdicke"] /= 1e-7
        gefilterte_values["Totschicht"] /= 1e-4
        gefilterte_values["activeLayer"] /= 1e-1

        #print("gefiltere",gefilterte_values)

        # Neue Instanz mit den gefilterten Werten erstellen
        return self.__class__(**gefilterte_values)


    def Minimierung_dark(self, Z_mittelwert,low_verteilung, **kwargs):
        def low_kon_be(low_kon, Verteilung):
            nor_vert = np.array(normiere_daten(Verteilung))
            return low_kon * nor_vert

        vorbereitete_Werte = kwargs.get("vorbereitete_Werte", None)
        if vorbereitete_Werte == None:
            vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Probenelemente = np.array(self.Probe1)
        index_low = np.where(Probenelemente<self.dark_M)
        index_high = np.where(Probenelemente>=self.dark_M)
        z_low = Probenelemente[index_low]
        z_high = Probenelemente[index_high]

        low_verteilung_volumenprozent = kwargs.get('low_verteilung_volumenprozent', False)
        if low_verteilung_volumenprozent:
            strings=[]
            zahlen=np.array(low_verteilung)
            for ele in z_low:
                strings.append(Element(Element=ele).Get_Elementsymbol())
            strings=np.array(strings)
            kombiniert = " + ".join(f"{z} {s}1" for z, s in zip(zahlen, strings))
            Elemente,low_verteilung, z = Verbindungen_Gewichtsprozent(kombiniert)

        binder = kwargs.get("binder", None) #([2,1,1],["1 H1O1", "2 He1O1 + 4 C1O4"]), in der From, erste eins für % der Probe hier 50/50, die anderen für die binder, binder nur Z<11, Binder in Massenprozent
        if binder is not None:
            konz_bind = np.zeros(len(self.Probe1))
            def Sym_Z(array):
                z=[]
                for i in array:
                    z.append(Element(Element=i).Get_Atomicnumber())
                return np.array(z)
            Verteilung_binder = normiere_daten(binder[0])
            for index, Verbind in enumerate(binder[1]):
                if Verbind[0].isdigit():
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent(Verbind)
                else:
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent("1"+Verbind)

                indices = np.array([np.where(Probenelemente == val)[0][0] for val in Sym_Z(ele)])
                konz_bind[indices] += np.array(konz) * Verteilung_binder[index+1]
            sum_konz_bind = konz_bind.sum()

        Startkonzentration = kwargs.get('Startkonzentration', None) #nur eine für low, die high konz
        if Startkonzentration == None:
            einstellung = {'Konzentration': self.Konzentration[index_high],
                           'P1': np.array(self.Probe1)[index_high],
                           'Übergänge': self.Übergänge[index_high].tolist()}
            klasse_ohne_low = self.klasse_erstellen(einstellung)
            konz, geo = klasse_ohne_low.Atiquant()


            #konz, geo = self.klasse_erstellen(einstellung).Atiquant()

            Startkonzentration = np.zeros(len(z_high)+1)
            Startkonzentration[1:] = konz

            x,y =Z_anpassen(np.zeros(len(z_low)),z_low, konz,z_high,Z_mittelwert)
            Startkonzentration[1:] *= y
            Startkonzentration[0] = x
            sum_high_start = Startkonzentration[1:].sum()

            if binder is None:
                konz_low_start = low_kon_be(Startkonzentration[0],low_verteilung)
            else:
                if sum_konz_bind >= Startkonzentration[0]/Startkonzentration.sum():
                    Startkonzentration[0] = sum_konz_bind*Startkonzentration.sum()
                konz_low_start = low_kon_be(Startkonzentration[0]-sum_konz_bind*Startkonzentration.sum(),low_verteilung)    #ohne /Konzentration.sum()?
                konz_low_start += konz_bind[index_low]*Startkonzentration.sum()
            #print("HIER")
            be_I_ati = klasse_ohne_low.Intensität_alle_jit_fürMinimierung(Startkonzentration[1:],)[0]*geo
            #be_I_ati *= self.Geo_IbIg(be_I_ati,np.arange(len(index_high)))
            #print(be_I_ati)
                  #self.Intensität_alle_jit_fürMinimierung(neue_Konz, vorbereitete_Werte)
            #print(self.Intensität_alle_jit_fürMinimierung(np.concatenate((konz_low_start, Startkonzentration[1:])), vorbereitete_Werte)[0]*geo)
            be_I_ati_O = ((self.Intensität_alle_jit_fürMinimierung(np.concatenate((konz_low_start, Startkonzentration[1:])), vorbereitete_Werte)[0]*geo)[index_high])
            #print(be_I_ati_O)
            #print(be_I_ati/be_I_ati_O)
            Startkonzentration[1:] *= be_I_ati/be_I_ati_O
            Startkonzentration[1:] *= sum_high_start / Startkonzentration[1:].sum()


            new_low_start, new_high_start = (Z_anpassen(konz_low_start, z_low, Startkonzentration[1:], z_high, Z_mittelwert))
            Startkonzentration[1:]*=new_high_start
            Startkonzentration[0]*=new_low_start
            konz_low_start*=new_low_start



 #           hmmm=((self.Intensität_alle_jit_fürMinimierung(np.concatenate((konz_low_start, Startkonzentration[1:])), vorbereitete_Werte)[0]*geo))
 #           hmmm *= self.Geo_IbIg(hmmm,index_high)
 #           print("ÜBERLEGTERSTART",hmmm)
  #          print(Startkonzentration)
  #          zzz=(np.concatenate((konz_low_start, Startkonzentration[1:])))
  #          print("STaRT")
   #         print(" & ".join([f"{value*100:.2f}" for value in zzz]))
   #         print(geo)
   #         print(self.Delta_I_konz(zzz,geo))
   #         Z_mittel_be = sum(con / np.concatenate((konz_low_start, Startkonzentration[1:])).sum() * self.Probe1[index]
    #        for index, con in enumerate(np.concatenate((konz_low_start, Startkonzentration[1:]))))
    #        print(Z_mittel_be)

        fix_konz = kwargs.get('fix_konz', None) # in prozent immer unter 100
        if fix_konz is not None:
            fix_konz=np.array(fix_konz)/100
            ent=np.arange(len(fix_konz))
            Startkonzentration = np.delete(Startkonzentration, ent+1)

            Zn = z_high[:len(fix_konz)] * fix_konz
            Zn=Zn.sum()
            Z_mittelwert = ((Z_mittelwert-Zn)/(1-fix_konz.sum()))
            z_high=z_high[len(fix_konz):]
            index_high=index_high[0][len(fix_konz):]


        gemessene_Intensitäten = self.Konzentration
        lower_bounds = np.zeros(len(Startkonzentration))
        upper_bounds = np.full(len(Startkonzentration), np.inf)



        def Residuen(params, gemessene_Intensitäten):
            def low_kon_be(low_kon, Verteilung):
                nor_vert = np.array(normiere_daten(Verteilung))
                return low_kon * nor_vert

            Konzentration = params[:]
            #Konzentration = normiere_daten(Konzentration)  #warum darf nicht machen????

            #if fix_konz != None:
            #    summe_fix=fix_konz.sum()/100
             #   neue_gesamtkon = Konzentration.sum()*(1+summe_fix)
             #   Konzentration=np.insert(Konzentration,1,fix_konz*neue_gesamtkon)

                #*für richtige Größenordnung!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            if binder is None:
                konz_low = low_kon_be(Konzentration[0],low_verteilung)
            else:
                if sum_konz_bind >= Konzentration[0]/Konzentration.sum():
                    Konzentration[0] = sum_konz_bind*Konzentration.sum()
                konz_low = low_kon_be(Konzentration[0]-sum_konz_bind*Konzentration.sum(),low_verteilung)
                konz_low += konz_bind[index_low]*Konzentration.sum()

            #konz_high = params[1:]
            konz_high = Konzentration[1:]
            new_low, new_high = (Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert))

            Konzentration[1:]*=new_high
            Konzentration[0]*=new_low

            if binder is None:
                neue_Konz = np.concatenate((low_kon_be(Konzentration[0],low_verteilung), Konzentration[1:]))
            else:
                neue_Konz = np.concatenate((konz_low*new_low, Konzentration[1:]))


            if fix_konz is not None:
                neue_gesamtkon = Konzentration.sum()*(1+fix_konz.sum())
                neue_Konz=np.insert(neue_Konz,len(low_verteilung),fix_konz*neue_gesamtkon)


            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(neue_Konz, vorbereitete_Werte)[0]

            berechnete_Intensitäten *= self.Geo_IbIg(berechnete_Intensitäten,index_high)

            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)

            if fix_konz is not None:
                ent=np.arange(len(fix_konz))
                gem_I, be_I = np.delete(gem_I, ent), np.delete(be_I, ent)
            #print("Konz",normiere_daten(np.array(neue_Konz))*100)

            return (be_I - gem_I)
            return (be_I - gem_I)/np.sqrt(be_I)
            #return (be_I - gem_I)/(be_I)

        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            max_nfev=100,
            args=(gemessene_Intensitäten,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        optimized_Konzentration = result.x[:]

        if binder is None:
            optimized_Konzentration = np.concatenate((np.array(low_kon_be(optimized_Konzentration[0],low_verteilung)), optimized_Konzentration[1:]))
        else:
            konz_low = np.array(low_kon_be(optimized_Konzentration[0]-sum_konz_bind*optimized_Konzentration.sum(),low_verteilung))
            konz_low += konz_bind[index_low]*optimized_Konzentration.sum()
            optimized_Konzentration = np.concatenate((konz_low, optimized_Konzentration[1:]))

        if fix_konz is not None:
            neue_gesamtkon = optimized_Konzentration.sum()*(1+fix_konz.sum())
            optimized_Konzentration=np.insert(optimized_Konzentration,len(low_verteilung),fix_konz*neue_gesamtkon)

        optimized_Geo = self.Geo_IbIg(self.Intensität_alle_jit_fürMinimierung(optimized_Konzentration, vorbereitete_Werte)[0] ,index_high)

        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        #print("Optimierter Geo-Wert:", optimized_Geo)
        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                  for index, con in enumerate(optimized_Konzentration))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        latex = kwargs.get('latex', False)
        if latex:
            self.Latex_tabel(values,self.Delta_I_konz(optimized_Konzentration,optimized_Geo,index_high),Z_mittel_be,optimized_Geo )
        else:
            print(" & ".join([f"{value:.4f}" for value in values]) + " & " + self.Delta_I_konz(optimized_Konzentration,optimized_Geo,index_high) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")



        return optimized_Konzentration, optimized_Geo

    def Latex_tabel(self,array,delta,Z,Geo):
        print("\\begin{table}","\\centering","\\resizebox{\\textwidth}{!}{","\\begin{tabular}{"+("|" + "c|" * (len(array)+4))+"}","\\hline", sep="\n")
        ele=[]
        for x in self.Probe1:
            ele.append(Element(Element=x).Get_Elementsymbol())
        print("Werte"+ " & "+(" & ".join([value for value in ele]))+" & "+" $ \\Delta$I & Z & Geo\\\\")
        print("\\hline")
        print("berechnet"+ " & "+(" & ".join([f"{value:.4f}" for value in array]))+" & "+delta+" & "+ f"{Z:.2f}" + " & "+ "{:.2e}".format(Geo)+" \\\\")
        print("\hline")
        print("\\end{tabular}","}","\\caption{test}","\\end{table}", sep="\n")



    def Spinat_test(self):

        #def Minimierung_dark(self, Z_mittelwert,low_verteilung

        Startwerte = [1,1,1,1,6.8]


        lower_bounds = np.zeros(len(Startwerte))
        upper_bounds = np.full(len(Startwerte), np.inf)

        lower_bounds[4]=6
        upper_bounds[4]=9

        Konz = np.array([0.5,0.5,2.9,1.52])
        ###Konz = np.array([0.0082,0.0012,0.0012,0.0055])  #2

        #params = Verteilung + Z
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()

        def Residuen(params, Konz,vorbereitete_Werte):

            optimized_Konzentration, optimized_Geo = self.Minimierung_dark(Z_mittelwert=params[-1],low_verteilung=params[:-1], vorbereitete_Werte=vorbereitete_Werte)
            #print(params)
            print(Konz)
            print()
            return optimized_Konzentration[4:8]-Konz
            ###return optimized_Konzentration[9:13]-Konz    #2  für schwere Elemente

        result = least_squares(
            Residuen,
            Startwerte,  # Startwerte für Konzentrationen und Geo
            max_nfev=100,
            args=(Konz,vorbereitete_Werte,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        print("ergebnis",result.x[:])

    def Spinat_test_fix(self):

        #def Minimierung_dark(self, Z_mittelwert,low_verteilung

        Startwerte = [3.5,81,1.18,8.2,6.2]


        lower_bounds = np.zeros(len(Startwerte))
        upper_bounds = np.full(len(Startwerte), np.inf)

        lower_bounds[4]=6
        upper_bounds[4]=9

        Konz = np.array([0.5,0.5,2.9,1.52])

        #params = Verteilung + Z
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()

        def Residuen(params, Konz,vorbereitete_Werte):

            optimized_Konzentration, optimized_Geo = self.Minimierung_dark(params[-1],params[:-1], vorbereitete_Werte=vorbereitete_Werte,fix_konz=[1.82,0.9])
            print(params)
            print(Konz)

            print(optimized_Konzentration[6:10],Konz)
            print()
            return optimized_Konzentration[6:10]-Konz

        result = least_squares(
            Residuen,
            Startwerte,  # Startwerte für Konzentrationen und Geo
            max_nfev=100,
            args=(Konz,vorbereitete_Werte,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        print("ergebnis",result.x[:])


    def Apple_test(self):
        Startwerte = [1,1,1,1,6]

        lower_bounds = np.zeros(len(Startwerte))
        upper_bounds = np.full(len(Startwerte), np.inf)

        lower_bounds[4]=5
        upper_bounds[4]=7

        Konz = np.array([0.16,0.18,1.6,1.52])

        #params = Verteilung + Z
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()

        def Residuen(params, Konz,vorbereitete_Werte):

            optimized_Konzentration, optimized_Geo = self.Minimierung_dark(params[-1],params[:-1], vorbereitete_Werte=vorbereitete_Werte)
            print(params)
            print(Konz)
            print()
            return optimized_Konzentration[4:8]-Konz

        result = least_squares(
            Residuen,
            Startwerte,  # Startwerte für Konzentrationen und Geo
            max_nfev=100,
            args=(Konz,vorbereitete_Werte,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        print(result.x[:])

    def Knochen_test(self):
        Startwerte = [1,1,1,1,12]
        Startwerte = [1.29871134, 11.33091673,  1.1731461,   1.37485863,11.5]

        lower_bounds = np.zeros(len(Startwerte))
        upper_bounds = np.full(len(Startwerte), np.inf)

        lower_bounds[4]=10
        upper_bounds[4]=14

        Konz = np.array([12.3,26.58])

        #params = Verteilung + Z
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()

        def Residuen(params, Konz,vorbereitete_Werte):

            optimized_Konzentration, optimized_Geo = self.Minimierung_dark(params[-1],params[:-1], vorbereitete_Werte=vorbereitete_Werte)
            print(params)
            print(Konz)
            print()
            return optimized_Konzentration[4:6]-Konz

        result = least_squares(
            Residuen,
            Startwerte,  # Startwerte für Konzentrationen und Geo
            max_nfev=100,
            args=(Konz,vorbereitete_Werte,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        print(result.x[:])



    def Minimierung_frei(self, Z_mittelwert, **kwargs):
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Probenelemente = np.array(self.Probe1)
        index_low = np.where(Probenelemente<self.dark_M)
        index_high = np.where(Probenelemente>=self.dark_M)
        z_low = Probenelemente[index_low]
        z_high = Probenelemente[index_high]

        Startkonzentration = kwargs.get('Startkonzentration', None)
        if Startkonzentration == None:
            einstellung = {'Konzentration': self.Konzentration[index_high],
                           'P1': np.array(self.Probe1)[index_high],
                           'Übergänge': self.Übergänge[index_high].tolist()}
            konz, geo = self.klasse_erstellen(einstellung).Atiquant()

            Startkonzentration = np.zeros(len(self.Konzentration))
            Startkonzentration[index_high] = konz

            x,y =Z_anpassen(np.zeros(len(z_low)),z_low, konz,z_high,Z_mittelwert)
            Startkonzentration[index_high] *= y
            Startkonzentration[index_low] = x/len(z_low)


        gemessene_Intensitäten = self.Konzentration

        lower_bounds = np.zeros(len(Startkonzentration))
        upper_bounds = np.full(len(Startkonzentration), np.inf)

        Bounds_prozent = kwargs.get('Bounds_prozent', None)#([array],float) float in Prozent 10=10%
        if Bounds_prozent != None:
            factor = float(Bounds_prozent[1]) / 100
            upper_bounds=np.array(Bounds_prozent[0])*(1+factor)
            lower_bounds = np.maximum(np.array(Bounds_prozent[0]) * (1 - factor), 0)  # Verhindert negative Werte
            lower_bounds = np.clip(lower_bounds, -np.inf, upper_bounds)
            upper_bounds = np.clip(upper_bounds, lower_bounds, np.inf)

            Startkonzentration = np.array(Startkonzentration, dtype=np.float64)
            Startkonzentration = np.clip(Startkonzentration, lower_bounds, upper_bounds)

        def Residuen1(params, gemessene_Intensitäten):
            print("🔍 Residuen-Aufruf mit params:", params)

            Konzentration = np.array(params, dtype=np.float64)  # Sichere Kopie

            # Check: Sind die Eingangsparameter gültig?
            if np.any(np.isnan(Konzentration)) or np.any(np.isinf(Konzentration)):
                print("❌ Fehler: NaN oder Inf in `params`!")
                return np.full_like(params, np.nan)

            konz_low = Konzentration[index_low]
            konz_high = Konzentration[index_high]

            print("🟢 Konzentration OK:", Konzentration)

            new_low, new_high = Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert)

            # Check: Sind `new_low` oder `new_high` ungültig?
            if np.any(np.isnan(new_low)) or np.any(np.isnan(new_high)):
                print("❌ Fehler: NaN in `Z_anpassen`-Rückgabe!")
                return np.full_like(params, np.nan)

            if np.any(np.isinf(new_low)) or np.any(np.isinf(new_high)):
                print("❌ Fehler: Inf in `Z_anpassen`-Rückgabe!")
                return np.full_like(params, np.nan)

            if np.any(new_low == 0) or np.any(new_high == 0):
                print("⚠️ Achtung: `new_low` oder `new_high` enthält Nullwerte!")

            print("🟢 `Z_anpassen` OK")

            Konzentration[index_high] *= new_high
            Konzentration[index_low] *= new_low

            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration, vorbereitete_Werte)[0]
            berechnete_Intensitäten *= self.Geo_IbIg(berechnete_Intensitäten, index_high)

            # Check: Sind `berechnete_Intensitäten` ungültig?
            if np.any(np.isnan(berechnete_Intensitäten)) or np.any(np.isinf(berechnete_Intensitäten)):
                print("❌ Fehler: NaN oder Inf in `berechnete_Intensitäten`!")
                return np.full_like(params, np.nan)

            print("🟢 `berechnete_Intensitäten` OK")

            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)

            # Check: Sind `be_I` oder `gem_I` ungültig?
            if np.any(np.isnan(be_I)) or np.any(np.isinf(be_I)) or np.any(np.isnan(gem_I)) or np.any(np.isinf(gem_I)):
                print("❌ Fehler: NaN oder Inf in `be_I` oder `gem_I`!")
                return np.full_like(params, np.nan)

            print("🟢 `be_I` und `gem_I` OK")

            # Division durch 0 verhindern
            Residuen_Werte = np.where(
                be_I != 0,
                (be_I - gem_I) / be_I,
                0  # Falls 0, setze Residuum auf 0 statt NaN/Inf
            )

            # Letzte Überprüfung: Sind die Residuen gültig?
            if np.any(np.isnan(Residuen_Werte)) or np.any(np.isinf(Residuen_Werte)):
                print("❌ Fehler: NaN oder Inf in `Residuen_Werte`!")
                return np.full_like(params, np.nan)

            print("✅ Residuen OK")
            return Residuen_Werte

        def Residuen(params, gemessene_Intensitäten):
            Konzentration = np.array(params, dtype=np.float64)

            konz_low = Konzentration[index_low]
            konz_high = Konzentration[index_high]
            new_low, new_high = (Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert))

            Konzentration[index_high]*=new_high
            Konzentration[index_low]*=new_low

            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration, vorbereitete_Werte)[0]
            berechnete_Intensitäten *= self.Geo_IbIg(berechnete_Intensitäten,index_high)

            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            #print(gem_I,be_I)

            #return (be_I - gem_I) / be_I
            return (be_I - gem_I)

        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            args=(gemessene_Intensitäten,),bounds=(lower_bounds, upper_bounds)
            ,xtol=1e-8,max_nfev=30,diff_step=1e-8 # Grenzen für Geo und Konzentration
    )
        optimized_Konzentration = result.x[:]
        optimized_Geo = self.Geo_IbIg(self.Intensität_alle_jit_fürMinimierung(optimized_Konzentration, vorbereitete_Werte)[0] ,index_high)
        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print("Optimierter Geo-Wert:", optimized_Geo)
        #print(len(self.Probe1),self.Probe1,len(optimized_Konzentration),optimized_Konzentration)
        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                  for index, con in enumerate(optimized_Konzentration))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + self.Delta_I_konz(optimized_Konzentration,optimized_Geo,index_high) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")
        #return optimized_Konzentration, optimized_Geo
        return values, optimized_Geo



    def Minimierung_frei_ohneZ(self,Startkonzentration,Bounds_prozent, **kwargs):#Bounds_prozen z.B. 10
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Probenelemente = np.array(self.Probe1)
        index_low = np.where(Probenelemente<self.dark_M)
        index_high = np.where(Probenelemente>=self.dark_M)
        z_low = Probenelemente[index_low]
        z_high = Probenelemente[index_high]

        gemessene_Intensitäten = self.Konzentration

        factor = float(Bounds_prozent[1]) / 100
        upper_bounds=np.array(Bounds_prozent[0])*(1+factor)
        lower_bounds = np.maximum(np.array(Bounds_prozent[0]) * (1 - factor), 0)  # Verhindert negative Werte
        lower_bounds = np.clip(lower_bounds, -np.inf, upper_bounds)
        upper_bounds = np.clip(upper_bounds, lower_bounds, np.inf)

        Startkonzentration = np.array(Startkonzentration, dtype=np.float64)
        Startkonzentration = np.clip(Startkonzentration, lower_bounds, upper_bounds)
        ##print("Lower",lower_bounds)
        ##print("upper",upper_bounds)


        def Residuen(params, gemessene_Intensitäten):
            Konzentration = np.array(params, dtype=np.float64)

            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration, vorbereitete_Werte)[0]
            berechnete_Intensitäten *= self.Geo_IbIg(berechnete_Intensitäten,index_high)

            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)

            return (be_I - gem_I)

        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            args=(gemessene_Intensitäten,),bounds=(lower_bounds, upper_bounds)
            ,xtol=1e-8,max_nfev=100#,diff_step=1e-8 # Grenzen für Geo und Konzentration
    )
        optimized_Konzentration = result.x[:]
        optimized_Geo = self.Geo_IbIg(self.Intensität_alle_jit_fürMinimierung(optimized_Konzentration, vorbereitete_Werte)[0] ,index_high)
        #print("sum-kon",optimized_Konzentration.sum())
        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])

        print("Optimierter Geo-Wert:", optimized_Geo)
        #print(len(self.Probe1),self.Probe1,len(optimized_Konzentration),optimized_Konzentration)
        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                  for index, con in enumerate(optimized_Konzentration))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + self.Delta_I_konz(optimized_Konzentration,optimized_Geo,index_high) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")
        #return optimized_Konzentration, optimized_Geo
        return values, optimized_Geo





    def Minimierung_var_Geo_Ati_fix_low(self, Z_mittelwert,low_verteilung, **kwargs):
        def low_kon_be(low_kon, Verteilung):
            nor_vert = np.array(normiere_daten(Verteilung))
            return low_kon * nor_vert

        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Probenelemente = np.array(self.Probe1)
        index_low = np.where(Probenelemente<self.dark_M)
        index_high = np.where(Probenelemente>=self.dark_M)
        z_low = Probenelemente[index_low]
        z_high = Probenelemente[index_high]

        low_verteilung_volumenprozent = kwargs.get('low_verteilung_volumenprozent', False)
        if low_verteilung_volumenprozent:
            strings=[]
            zahlen=np.array(low_verteilung)
            for ele in z_low:
                strings.append(Element(Element=ele).Get_Elementsymbol())
            strings=np.array(strings)
            kombiniert = " + ".join(f"{z} {s}1" for z, s in zip(zahlen, strings))
            Elemente,low_verteilung, z = Verbindungen_Gewichtsprozent(kombiniert)


        binder = kwargs.get("binder", None) #([2,1,1],["1 H1O1", "2 He1O1 + 4 C1O4"]), in der From, erste eins für % der Probe hier 50/50, die anderen für die binder, binder nur Z<11, Binder in Massenprozent
        if binder is not None:
            konz_bind = np.zeros(len(self.Probe1))
            def Sym_Z(array):
                z=[]
                for i in array:
                    z.append(Element(Element=i).Get_Atomicnumber())
                return np.array(z)
            Verteilung_binder = normiere_daten(binder[0])
            for index, Verbind in enumerate(binder[1]):
                #print(Verbind)
                if Verbind[0].isdigit():
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent(Verbind)
                else:
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent("1"+Verbind)

            #print("binder",konz)

                #indices = np.where(np.isin(z_low, Sym_Z(ele)))[0]
                indices = np.array([np.where(Probenelemente == val)[0][0] for val in Sym_Z(ele)])
                #print(Verteilung_binder[index+1])
                konz_bind[indices] += np.array(konz) * Verteilung_binder[index+1]
            sum_konz_bind = konz_bind.sum()
            #print(konz_bind)

        Startkonzentration = kwargs.get('Startkonzentration', None) #nur eine für low, die high konz und geo
        if Startkonzentration == None:
            einstellung = {'Konzentration': self.Konzentration[index_high],
                           'P1': np.array(self.Probe1)[index_high],
                           'Übergänge': self.Übergänge[index_high].tolist()}
            konz, geo = self.klasse_erstellen(einstellung).Atiquant()

            Startkonzentration = np.zeros(len(z_high)+2)
            Startkonzentration[1:-1] = konz

            x,y =Z_anpassen(np.zeros(len(z_low)),z_low, konz,z_high,Z_mittelwert)
            #Startkonzentration[index_high] *= y
            Startkonzentration[1:-1] *= y
            #print("Atigeo",geo)
            Startkonzentration[-1] = geo*(1+1*x)
            Startkonzentration[0] = x

            #Für Geometriefaktor

            if binder is None:
                Start_konz = np.concatenate((low_kon_be(Startkonzentration[0],low_verteilung), Startkonzentration[1:-1]))
            else:
                konz_low_start = low_kon_be(Startkonzentration[0]-sum_konz_bind*Startkonzentration.sum(),low_verteilung)    #ohne /Konzentration.sum()?
                konz_low_start += konz_bind[index_low]*Startkonzentration.sum()
                Start_konz = np.concatenate((konz_low_start, Startkonzentration[1:-1]))
            werte_start=self.Intensität_alle_jit_fürMinimierung(Start_konz, vorbereitete_Werte)[0]

            #print("GEO_ALT",Startkonzentration[-1],"NEU",self.Geo_IbIg(werte_start,index_high))
            #print(werte_start*self.Geo_IbIg(werte_start,index_high))
            #print(self.Konzentration)
            Startkonzentration[-1] = self.Geo_IbIg(werte_start,index_high)
            #Startkonzentration[-1] = 5.3162754125033176e-06


        gemessene_Intensitäten = self.Konzentration
        Geo = Startkonzentration[-1]

        lower_bounds = np.zeros(len(Startkonzentration))
        upper_bounds = np.full(len(Startkonzentration), np.inf)

        #if dark_bounds_lower is not None:
        #    lower_bounds[index_low] = dark_bounds_lower

        #print("start",Startkonzentration)
        #print("start",Startkonzentration)
        #print(gemessene_Intensitäten)

        #Geo_weite = kwargs.get('Geo_bound', 0.2)
        #Grenze = Geo * np.abs(Geo_weite)

        #if (Geo_weite >=1 or Geo_weite < 0):
        #    lower_bounds[-1] = 0
        #    upper_bounds[-1] = Geo + Grenze
        #else:
        #    lower_bounds[-1] = Geo - Grenze
         #   upper_bounds[-1] = Geo + Grenze


        iteration_counter = 0  # Zähler für Iterationen
        #print("Startwerte",Startkonzentration)

        def Residuen(params, gemessene_Intensitäten):

            nonlocal iteration_counter
            iteration_counter += 1
            #print(f"Iteration: {iteration_counter}")
            #if iteration_counter >= 100:
            #    return np.ones_like(params) * 1e6  # Schlechte Werte zurückgeben → Abbruch erzwingen

            def low_kon_be(low_kon, Verteilung):
                nor_vert = np.array(normiere_daten(Verteilung))
                return low_kon * nor_vert
            #print("para",params)

            Konzentration = params[:-1]
            #print(sum_konz_bind)
            #print(Konzentration.sum())
           # Konzentration=normiere_daten(Konzentration)
            if binder is None:
                konz_low = low_kon_be(Konzentration[0],low_verteilung)
            else:
                if sum_konz_bind >= Konzentration[0]/Konzentration.sum():
                    Konzentration[0] = sum_konz_bind*Konzentration.sum()
                konz_low = low_kon_be(Konzentration[0]-sum_konz_bind*Konzentration.sum(),low_verteilung)    #ohne /Konzentration.sum()?
                konz_low += konz_bind[index_low]*Konzentration.sum()

            konz_high = params[1:-1]#Konzentration[1:]
            #konz_high = Konzentration[1:]
            new_low, new_high = (Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert))
            Konzentration[1:]*=new_high
            Konzentration[0]*=new_low

            if binder is None:
                neue_Konz = np.concatenate((low_kon_be(Konzentration[0],low_verteilung), Konzentration[1:]))
            else:
                neue_Konz = np.concatenate((konz_low*new_low, Konzentration[1:]))
                #print("konz_low,new_low",konz_low,new_low)

            Geo = params[-1]
            #print("geo",Geo)
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(neue_Konz, vorbereitete_Werte)[0] * Geo
            #print("int",berechnete_Intensitäten)
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            #print("NeueKOnz",neue_Konz,Geo,"RES",(be_I - gem_I))
            #print(self.Delta_I(be_I,gem_I))
            #print(params[:4],Geo)
            #print(Geo)
            return (be_I - gem_I)
            #return (be_I - gem_I)/np.sqrt(be_I)


        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            max_nfev=30,
            args=(gemessene_Intensitäten,),bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
            )

        optimized_Konzentration = result.x[:-1]
        #print(low_kon_be(optimized_Konzentration[0],low_verteilung), optimized_Konzentration[1:])
        if binder is None:
            optimized_Konzentration = np.concatenate((np.array(low_kon_be(optimized_Konzentration[0],low_verteilung)), optimized_Konzentration[1:]))
        else:
            konz_low = np.array(low_kon_be(optimized_Konzentration[0]-sum_konz_bind*optimized_Konzentration.sum(),low_verteilung))
            konz_low += konz_bind[index_low]*optimized_Konzentration.sum()
            optimized_Konzentration = np.concatenate((konz_low, optimized_Konzentration[1:]))



        optimized_Geo = result.x[-1]
        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print("Optimierter Geo-Wert:", optimized_Geo)
        #print("solltegleichseingeo",self.Geo_IbIg(self.Intensität_alle_jit_fürMinimierung(optimized_Konzentration, vorbereitete_Werte)[0],index_high))
        print("delta",self.Delta_I_konz(optimized_Konzentration,self.Geo_IbIg(self.Intensität_alle_jit_fürMinimierung(optimized_Konzentration, vorbereitete_Werte)[0],index_high)))
        #print("op_konz",optimized_Konzentration)

        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                  for index, con in enumerate(optimized_Konzentration))

        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + self.Delta_I_konz(optimized_Konzentration,optimized_Geo) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")

        return optimized_Konzentration, optimized_Geo


    def Geo_IbIg(self,Ib,indices):#indices um 0/0 zu verhindern
        np_Ib, np_Ig = np.array(Ib), np.array(self.Konzentration)
        ratios = np_Ig[indices] / np_Ib[indices] # Elementweise Division
        k_opt = np.median(ratios)  # Median der Verhältnisse
        return k_opt



    def Minimierung_var_Geo_Ati(self, Z_mittelwert, **kwargs):
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Probenelemente = np.array(self.Probe1)
        index_low = np.where(Probenelemente<self.dark_M)
        index_high = np.where(Probenelemente>=self.dark_M)
        z_low = Probenelemente[index_low]
        z_high = Probenelemente[index_high]

        binder = kwargs.get("binder", None) #([2,1,1],["1 H1O1", "2 He1O1 + 4 C1O4"]), in der From, erste eins für % der Probe hier 50/50, die anderen für die binder, binder nur Z<11, Binder in Massenprozent
        if binder is not None:
            konz_bind = np.zeros(len(self.Probe1))
            def Sym_Z(array):
                z=[]
                for i in array:
                    z.append(Element(Element=i).Get_Atomicnumber())
                return np.array(z)
            Verteilung_binder = normiere_daten(binder[0])
            for index, Verbind in enumerate(binder[1]):
                if Verbind[0].isdigit():
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent(Verbind)
                else:
                    ele, konz, z = Verbindungen_Gewichtsprozent_vonMassenprozent("1"+Verbind)
                indices = np.array([np.where(Probenelemente == val)[0][0] for val in Sym_Z(ele)])
                konz_bind[indices] += np.array(konz) * Verteilung_binder[index+1]
            sum_konz_bind = konz_bind.sum()


        Startkonzentration = kwargs.get('Startkonzentration', None)
        if Startkonzentration == None:
            #Geo * 2 * Z_low_konz
            #pass
            #konz, geo = self.Atiquant()
            #print(konz,geo)
            #print(np.append(konz, geo[0]))

            #print(self.Probe1)
            #print(np.array2string(self.Konzentration[index_high], separator=', '))
            #einstellung =

            #einstellung="Konzentration="+str(np.array2string(self.Konzentration[index_high], separator=', '))+", P1="+str(np.array2string(np.array(self.Probe1)[index_high], separator=', ') + ", Übergänge=" +str(np.array2string(np.array(self.Übergänge)[index_high], separator=', ')))
            #print(einstellung)
            einstellung = {'Konzentration': self.Konzentration[index_high],
                           'P1': np.array(self.Probe1)[index_high],
                           'Übergänge': self.Übergänge[index_high].tolist()}
            konz, geo = self.klasse_erstellen(einstellung).Atiquant()
            #self.klasse_erstellen(einstellung).Atiquant()
            #self.klasse_erstellen(einstellung).Atiquant()
            #print(konz, geo)
            #konz, geo = call_class_with_config_2(self.__class__, einstellung).Atiquant()
            Startkonzentration = np.zeros(len(self.Konzentration)+1)
            Startkonzentration[index_high] = konz

            #print(konz[0])
            #Startwerte = [0,x, 0.11413267*y, 0.88586733*y, 4.73747169e-06*(1+2*x)]
            #(konz_low, z_low, konz_high, z_high, z_gewünscht)
            #print(np.zeros(len(z_low)),z_low, konz,z_high,Z_mittelwert)
            x,y =Z_anpassen(np.zeros(len(z_low)),z_low, konz,z_high,Z_mittelwert)
            Startkonzentration[index_high] *= y
            Startkonzentration[-1] = geo*(1+2*x)
            Verteilung = kwargs.get('Verteilung', None)
            if Verteilung == None:
                Startkonzentration[index_low] = x/len(z_low)
            else:
                Verteilung = [norm /np.array(Verteilung).sum() for norm in Verteilung]
                #print(Verteilung)
                index_low_list = index_low[0].tolist()
                for index, wert in enumerate(Verteilung):
                    #print(wert)
                    #print(index_low)
                   # print(index_low_list[index])
                    Startkonzentration[index_low_list[index]] = x * wert

            #print(Startkonzentration)

            #for i in index_low:
             #   np.insert(Startkonzentration, i, 0)
            #print(Startkonzentration)

        gemessene_Intensitäten = self.Konzentration
        Geo = Startkonzentration[-1]
        Geo_weite = kwargs.get('Geo_bound', 1)

        lower_bounds = np.zeros(len(Startkonzentration))
        upper_bounds = np.full(len(Startkonzentration), np.inf)

        Grenze = Geo * np.abs(Geo_weite)
        if (Geo_weite >=1 or Geo_weite < 0):
            lower_bounds[-1] = 0
            upper_bounds[-1] = Geo + Grenze
        else:
            lower_bounds[-1] = Geo - Grenze
            upper_bounds[-1] = Geo + Grenze

        low_fix = kwargs.get('low_fix', None)
        if low_fix != None:
            fix_bounds = kwargs.get('fix_bounds', 0.05) # in Prozent
            low_fix = np.array([norm /np.array(low_fix).sum() for norm in low_fix])
            low_bound_lower = np.maximum(low_fix - fix_bounds, 0)
            low_bound_upper = low_fix + fix_bounds

        Bounds_prozent = kwargs.get('Bounds_prozent', None)#([array],float) float in Prozent 10=10%
        if Bounds_prozent != None:
            factor = float(Bounds_prozent[1]) / 100
            #lower_bounds=np.array(Bounds_prozent[0])*(1-factor)
            upper_bounds=np.array(Bounds_prozent[0])*(1+factor)
            lower_bounds = np.maximum(np.array(Bounds_prozent[0]) * (1 - factor), 0)  # Verhindert negative Werte

            lower_bounds = np.clip(lower_bounds, -np.inf, upper_bounds)
            upper_bounds = np.clip(upper_bounds, lower_bounds, np.inf)
            #lower_bounds[-1]=0
            #upper_bounds[-1]=1
            print("lower_bounds",lower_bounds)
            print("upper_bounds",upper_bounds)


        Startkonzentration = np.array(Startkonzentration, dtype=np.float64)
        Startkonzentration = np.clip(Startkonzentration, lower_bounds, upper_bounds)

        def Residuen(params, gemessene_Intensitäten):
            nonlocal low_fix

            Konzentration = params[:-1]
            #print("kondavor",normiere_daten(Konzentration))
            #print("SUMME_davor",Konzentration.sum())

            if binder is None:
                konz_low = Konzentration[index_low]
            else:

                konz_low = Konzentration[index_low]
                save=konz_low.copy()

                bedingung = konz_bind[index_low] * Konzentration.sum()
                bedingung_bool = bedingung>konz_low  #wird zu true false array
                konz_low = np.where(bedingung>konz_low,bedingung,konz_low)
                if np.any(save != konz_low):
                    konz_dif = konz_low.sum() - save.sum()
                    false_indices = np.where(bedingung_bool == False)[0]
                    anzahl_false = np.sum(~bedingung_bool)
                    konz_low[false_indices] -= konz_dif/anzahl_false


            konz_high = Konzentration[index_high]
            new_low, new_high = (Z_anpassen(konz_low, z_low, konz_high, z_high, Z_mittelwert))

            #if low_fix is not None and low_fix.size > 0:
               # Konzentration[index_low]=(low_fix * new_low + new_low * konz_low)/2
                #low_fix = new_low * konz_low
            Konzentration[index_high]*=new_high

            ##if low_fix is not None and low_fix.size > 0:

            ##    Konzentration[index_low]*=new_low
                #gesamtkonz = Konzentration.sum()
                #print("neu_kon",normiere_daten(Konzentration[index_low]))
            ##    Konzentration[index_low]=Grenzen_fix(Konzentration[index_low],low_fix,fix_bounds)
               # print("gebounded",normiere_daten(Konzentration[index_low]),"Geo",params[-1])
                #Konzentration[index_low]=np.clip(Konzentration[index_low], low_bound_lower*new_low*gesamtkonz, low_bound_upper*new_low*gesamtkonz)
            ##else:
            #print("vornewlow",normiere_daten(Konzentration))

            Konzentration[index_low]*=new_low

            #print("SUMME",Konzentration.sum())
            #print(normiere_daten(Konzentration))

            Geo = params[-1]
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration, vorbereitete_Werte)[0] * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)
            #print("para",params,"res",(be_I - gem_I))
            #return (be_I - gem_I)
            #if dark_bounds_lower is not None:
             #   params[:-1]=normiere_daten(params[:-1])


            ##if Bounds_prozent != None:
            ##    start = np.clip(start, lower_bounds, upper_bounds)

            return (be_I - gem_I) / be_I


        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            args=(gemessene_Intensitäten,),bounds=(lower_bounds, upper_bounds)
            ,xtol=1e-8,max_nfev=30,diff_step=1e-8 # Grenzen für Geo und Konzentration
    )

        optimized_Konzentration = result.x[:-1]
        optimized_Geo = result.x[-1]
        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print("Optimierter Geo-Wert:", optimized_Geo)
        #print("op_konz",optimized_Konzentration)

        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                  for index, con in enumerate(optimized_Konzentration))

        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + self.Delta_I_konz(optimized_Konzentration,optimized_Geo) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")


        #return optimized_Konzentration, optimized_Geo
        return values, optimized_Geo

    def Minimierung_var_Geo(self, Geo, Z_Gewichtung=1, **kwargs):
        vorbereitete_Werte = self.Werte_vorbereiten_alle_jit()
        Startkonzentration = kwargs.get('Startkonzentration', None)
        if Startkonzentration != None:
            Startkonzentration = np.array([con / np.array(Startkonzentration).sum() for con in Startkonzentration] + [Geo])
        else:
            Startkonzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration] + [Geo])
        gemessene_Intensitäten = self.Konzentration
        Z_gemittelt = kwargs.get('Z_gemittelt', None)
        Geo_weite = kwargs.get('Geo_bound', 1)

        lower_bounds = np.zeros(len(Startkonzentration))
        upper_bounds = np.full(len(Startkonzentration), np.inf)
        Grenze = Geo * np.abs(Geo_weite)
        if (Geo_weite >=1 or Geo_weite < 0):
            lower_bounds[-1] = 0
            upper_bounds[-1] = Geo + Grenze
        else:
            lower_bounds[-1] = Geo - Grenze
            upper_bounds[-1] = Geo + Grenze
        #print("geo",Geo)
        #print(Geo*0.9)
        #print("lower",lower_bounds[-1], "upper", upper_bounds[-1])

        iteration = 0

        def Residuen(params, gemessene_Intensitäten):
            nonlocal iteration
            Konzentration = params[:-1]
            Geo = params[-1]
            berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration, vorbereitete_Werte)[0] * Geo
            Auslassen = [index for index, i in enumerate(berechnete_Intensitäten) if i == 0]
            gem_I, be_I = np.delete(gemessene_Intensitäten, Auslassen), np.delete(berechnete_Intensitäten, Auslassen)

            # Berechnung des Residuenwerts
            #print(params)
            if Z_gemittelt is not None:
                Konz_norm = np.array([con /Konzentration.sum() for con in Konzentration])
                Z_gem_be = sum(con * self.Probe1[index] for index, con in enumerate(Konz_norm))
                Z_gemittelt_array = np.full(len(Konzentration)-len(Auslassen), Z_gemittelt)
                Z_gem_be_array = np.full(len(Konzentration)-len(Auslassen), Z_gem_be)


                fehler = abs(Z_gem_be - Z_gemittelt)  # Differenz
                fehler_relativ = (Z_gem_be - Z_gemittelt) / Z_gem_be  # Relativer Fehler
                global weighting
                if iteration == 0:
                    weighting = 0  # Startwert für Gewichtung

                if iteration % 3 == 0:

                    if np.all(fehler < 0.1):  # Falls der Fehler unter 1% bleibt
                        weighting *= 0.9  # Gewichtung langsam reduzieren
                    elif np.all(fehler > 0.2):  # Falls Fehler extrem klein ist
                        weighting *= 1.1  # Gewichtung stark reduzieren
                #else:
                  #  weighting *= 1.1  # Falls der Fehler über 1% bleibt, Gewichtung erhöhen

                weighting = max(0.1, min(weighting, 3))  # Begrenzung zwischen 0.1 und 10, damit es nicht explodiert

                iteration += 1  # Iterationszähler erhöhen
                #print(weighting, fehler)
                #print(Konz_norm)

                #print(berechnete_Intensitäten)
                #print(Konz_norm)

                #return np.abs((np.log(be_I) - np.log(gem_I)) / np.log(be_I)) + \
                  #     np.log(np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array)))
                #return (be_I - gem_I) / be_I * (Z_gem_be_array - Z_gemittelt_array)
                #print(np.abs((be_I - gem_I) / be_I),"zu",np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array)))
                #print(np.log(np.abs((be_I - gem_I) / be_I)))
                #return np.abs((be_I - gem_I) / be_I) + np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array))

                return np.abs((be_I - gem_I) / be_I**(1/2)) + np.abs(weighting * Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array) * be_I**(1/2))
                #return np.abs((be_I - gem_I) / be_I * np.maximum(be_I/gem_I,gem_I/be_I)) + np.abs( Z_Gewichtung* (Z_gem_be_array - Z_gemittelt_array))

                #return np.abs((be_I - gem_I) / be_I) + np.abs( np.maximum(Z_gem_be_array /Z_gemittelt_array,Z_gemittelt_array/Z_gem_be_array ) * (Z_gem_be_array - Z_gemittelt_array))

                #print(np.abs((be_I - gem_I) / be_I),"zu",np.abs(Z_Gewichtung * (Z_gem_be_array - Z_gemittelt_array)))
                #return np.abs((be_I - gem_I) / be_I**(1/2) * np.maximum(be_I/gem_I,gem_I/be_I)) + np.abs(np.maximum(Z_gem_be_array/Z_gemittelt_array,Z_gemittelt_array/Z_gem_be_array) * (Z_gem_be_array - Z_gemittelt_array) * be_I**(1/2))

            return (be_I - gem_I) / be_I


        #while iteration < 300:
        # Optimierung mit least_squares, Geo als Teil der Startkonzentrationen
        result = least_squares(
            Residuen,
            Startkonzentration,  # Startwerte für Konzentrationen und Geo
            args=(gemessene_Intensitäten,),
            bounds=(lower_bounds, upper_bounds),xtol=1e-8 # Grenzen für Geo und Konzentration
    )
        iteration += 1


        # Extrahiere die optimierten Konzentrationen und den Geo-Wert
        optimized_Konzentration = result.x[:-1]
        optimized_Geo = result.x[-1]
        optimized_Konzentration = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])


        # Zusätzliche Berechnungen und Ausgabe
        Z_mittel_be = sum(con / optimized_Konzentration.sum() * self.Probe1[index]
                          for index, con in enumerate(optimized_Konzentration))
        print("Optimierter Geo-Wert:", optimized_Geo)
        if Z_gemittelt is not None:
            print("Mit Z_gemittelt", Z_gemittelt, "Gewichtung", Z_Gewichtung)
        else:
            print("Ohne Z_gemittelt")
        #print("Optimierte Konzentrationen NORMIERT NLLS in %:",
        #      np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration]))
        values = np.array([con / optimized_Konzentration.sum() * 100 for con in optimized_Konzentration])
        print(" & ".join([f"{value:.2f}" for value in values]) + " & " + "{:.2e}".format(result.cost) + " & " + f"{Z_mittel_be:.2f}" + " & " + "{:.2e}".format(optimized_Geo)+" \\\\")#
       # print("Anzahl der Funktionsauswertungen:", result.nfev)
        #print("Kosten (Summe der quadrierten Residuen):", result.cost)
        return optimized_Konzentration, optimized_Geo

    def Delta_I(self, Ig, Ib):
        Ig, Ib = np.array(Ig), np.array(Ib)
        delta = Ig - Ib
        return "{:.2e}".format(np.sum(np.abs(delta)))  # Gibt das Ergebnis als String zurück

    def Delta_I_konz(self,konz,geo,indices):#konz + geo
        Ig = np.array(self.Konzentration)
        Ib = np.array(self.Intensität_alle_jit_fürMinimierung(konz)[0])*geo
        delta = Ig[indices] - Ib[indices]
        return "{:.2e}".format(np.sum(np.abs(delta)))

    def Kosten(self, Konzentration, Geo):
        gemessene_Intensitäten = self.Konzentration
        berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration)[0] * Geo


        # Berechnung der Residuen wie in der Minimierungsfunktion
        residuen = (berechnete_Intensitäten - gemessene_Intensitäten) / np.sqrt(berechnete_Intensitäten)
        ##residuen = (berechnete_Intensitäten - gemessene_Intensitäten) / np.sqrt(gemessene_Intensitäten)

        print("Konzentration",Konzentration,"Kosten=ChiSquare",0.5 * np.sum(residuen**2))

        # Kosten basieren auf der Summe der quadrierten Residuen
        return 0.5 * np.sum(residuen**2)


    def Kosten_2(self, Konzentration, Geo):
        gemessene_Intensitäten = self.Konzentration
        berechnete_Intensitäten = self.Intensität_alle_jit_fürMinimierung(Konzentration) * Geo


        residuen = (berechnete_Intensitäten / gemessene_Intensitäten)
        Mittelwert = np.mean(residuen)

        print("Konzentration",Konzentration,"Kosten=ChiSquare",0.5 * np.sum((residuen - Mittelwert)**2), "berechnete Intensiät",berechnete_Intensitäten)

        return 0.5 * np.sum((residuen - Mittelwert)**2)

    def Kalibrierung_nlls(self, para_var, grenzen, gemessene_Intensität, Elemente, Übergänge, para = None, Bedingung=False, **kwargs):   #Reinelemente
            if "Startwerte" in kwargs:
                Startwerte = kwargs["Startwerte"]  # Übernehme Startwerte aus kwargs
            else:
                # Generiere zufällige Startwerte, falls nicht vorhanden
                Startwerte = [np.random.uniform(low, high) for low, high in grenzen]
            lower_bounds, upper_bounds = zip(*grenzen)
            print(lower_bounds, upper_bounds)
            if "method" in kwargs:
                method = kwargs["method"]
            else:
                method = "trf"
            #Elemente_ordnungszahl = [int(Element(Element=ele).Get_Atomicnumber()) for ele in Elemente]
            Elemente_symbol = [Element(Element=ele).Get_Elementsymbol() for ele in Elemente]
            def Residuen(para_res, gemessene_Intensität):
                berechnete_Intensität = []
                for index_ele, ele in enumerate(Elemente_symbol):
                    parts=[]
                    for index, par in enumerate(para_var):
                        parts.append(par[0] + "=" + f"{para_res[index]:.8e}")

                    if Bedingung:
                        for index, x in enumerate(para_var):
                            if para_var[index][0] == "Einfallswinkelalpha":
                                parts.append("Einfallswinkelbeta" + "=" + f"{90-para_res[index]:.8e}")
                                break
                            if para_var[index][0] == "Einfallswinkelbeta":
                                parts.append("Einfallswinkelalpha" + "=" + f"{90-para_res[index]:.8e}")
                                break

                    var_einstellung = ", ".join(parts)
                    var_einstellung+= ", P1=['"+str(ele)+"']"
                    var_einstellung+= ", Übergänge=["+str(Übergänge[index_ele])+"]"
                    if para != None:
                        var_einstellung+=", "+para

                    ##print(var_einstellung)
                    berechnete_Intensität.append(call_class_with_config(self.__class__, var_einstellung).Intensität_alle_jit_fürMinimierung([1])[0][0])
                berechnete_Intensität = np.array(berechnete_Intensität)
                Geo = np.array(gemessene_Intensität)/berechnete_Intensität
                Mittelwert = np.mean(Geo)
                residuen = np.mean(np.abs(Geo - Mittelwert)) / Mittelwert
                #residuen = np.mean(np.abs(Geo - Mittelwert))        #ohne relative
                print(f"Residuen: {residuen}, para_res: {para_res}")
                if method =="lm":
                    residuen = (Geo - Mittelwert) / Mittelwert
                return residuen
                #return np.mean(np.abs(Geo - Mittelwert))/Mittelwert    #np.mean(np.abs(Geo - Mittelwert))/Mittelwert   wäre % abweichung
            ##Residuen(Startwerte,gemessene_Intensität)

            print("Teste Residuen bei Startwerten:", Startwerte)
            resid = Residuen(Startwerte, gemessene_Intensität)
            print("Residuen:", resid)
            print("Alle endlich?", np.all(np.isfinite(resid)))


            if (method == "lm"):
                result = least_squares(
                Residuen,
                Startwerte,  # Startwerte für Konzentrationen
                args=( gemessene_Intensität,), # Übergabe des Modells und der gemessenen Daten
                method='dogbox',
                max_nfev=10
                )
                optimized_Konzentration = result.x
                return optimized_Konzentration
            else:
                result = least_squares(
                Residuen,
                Startwerte,  # Startwerte für Konzentrationen
                args=( gemessene_Intensität,),bounds=(lower_bounds, upper_bounds),  # Übergabe des Modells und der gemessenen Daten
                max_nfev=10
                )
                optimized_Konzentration = result.x
                return optimized_Konzentration



    def Werte_vorbereiten_alle(self,alle_Probenelemente):#Lochtransfer später
        #Probe = Probeneingabe(alle_Probenelemente)
        Probe = Probeneingabe(self.Probe1)
        Elementliste = []
        alle_Übergänge = []
        alle_Kanten = []
        for i in Probe:#i=Element
            erstellte_Element = Element(Dateipfad=self.Dateipfad, Element=i, Emin = self.Emin, Emax = self.Emax, step = self.step)
            Elementliste.append(erstellte_Element)
            alle_Kanten.append([Kante[1] for Kante in erstellte_Element.Kanten()[0:4]])
            if erstellte_Element.Ubergange() == [[]]:
                alle_Übergänge.append([])
            else:
                alle_Übergänge.append([(str_zu_zahl(Über[0]), Über[1], Über[2]) for Über in erstellte_Element.Ubergange()])
        Tube0, Tau0, Omega0, Mü0, Sij0 = [], [], [], [], []
        Tau, Mü = [], []
        Tau_ijk, Mü_ijk = [], []
        Det_ijk = []
        Sij, Sij_xyz = [], []
        for index, x_Element in enumerate(Elementliste):
            Tube0_anhang, Tau0_anhang, Omega0_anhang, Sij0_anhang, Sij_anhang= [], [], [], [], []
            for Kantenindex, Energie in enumerate(alle_Kanten[index]):
                step = (int(Energie/self.step)+1)*self.step - Energie
                if (Energie==0):
                    Energie=0.000001
                Tube0_anhang.append(self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0])
                Tau0_anhang.append(x_Element.Massenabsorptionskoeffizient(Energie)[1][0])
                Sij0_anhang.append(x_Element.S_ij(x_Element.Kanten()[Kantenindex][0], Energie))
                Omega0_anhang.append(x_Element.Omega_Schale(x_Element.Kanten()[Kantenindex][0]))
                #Mü0_anhang.append(x_Element.Massenschwächungskoeffizient(Energie)[1][0])
                Sij_Kante = np.array([x_Element.S_ij(x_Element.Kanten()[Kantenindex][0][0:2], k * self.step) for k in range(int(Energie/self.step + 1), int(self.Emax/self.step + 1))])
                Sij_anhang.append(Sij_Kante)
                Sij_xyz_anhang = (np.array([x_Element.S_ij(x_Element.Kanten()[Kantenindex][0][0:2], Ubergang[1]) for Ubergang in alle_Übergänge[index]]))
                Sij_xyz.append(Sij_xyz_anhang)
            Tube0.append(Tube0_anhang)
            Tau0.append(Tau0_anhang)
            Omega0.append(Omega0_anhang)
            Mü0.append([[x_Element.Massenschwächungskoeffizient(Kante)[1][0] for Kante in Kanten] for Kanten in alle_Kanten])
            Sij0.append(Sij0_anhang)
            Sij.append(Sij_anhang)
            Tau.append(x_Element.tau[1])
            Mü.append(x_Element.mü[1])
            Mü_ijk_anhang, Tau_ijk_anhang = [], []
            for index_Über, Über in enumerate(alle_Übergänge):
                if (index == 0 and Über != []):
                    Det_ijk_anhang = [self.Detektor.Detektoreffizienz(x[1]) for x in Über]
                if (index == 0 and Über == []):
                    Det_ijk_anhang = []
                if (index==0):
                    Det_ijk.append(Det_ijk_anhang)
                if (Über != []):
                    Mü_ijk_anhang.append([x_Element.Massenschwächungskoeffizient(x[1])[1][0] for x in Über])
                    Tau_ijk_anhang.append([x_Element.Massenabsorptionskoeffizient(x[1])[1][0] for x in Über])
                else:
                    Mü_ijk_anhang.append([])
                    Tau_ijk_anhang.append([])
            Mü_ijk.append(Mü_ijk_anhang)
            Tau_ijk.append(Tau_ijk_anhang)

        Countrate = self.Röhre.Countrate_gesamt[1]
        try:
            Konzentration = np.array([con / self.Konzentration.sum() for con in self.Konzentration])
        except:
            print("keine Konzentrationen eingegeben")

        #return Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Mü_ijk, Det_ijk, Sij, alle_Kanten, alle_Übergänge, Sij_xyz, Tau_ijk, Konzentration, self.step, self.Emin
        return np.array(Tube0), np.array(Tau0), np.array(Omega0), np.array(Mü0), np.array(Sij0), np.array(Tau), np.array(Mü), np.array(Countrate), np.array(Mü_ijk, dtype=object), np.array(Det_ijk, dtype=object), np.array(Sij, dtype=object), np.array(alle_Kanten), np.array(alle_Übergänge, dtype=object), np.array(Sij_xyz, dtype=object), np.array(Tau_ijk, dtype=object), np.array(Konzentration), self.step, self.Emin

    def Primärintensität_berechnen_alle(self, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Mü_ijk, Det_ijk, Sij, alle_Kanten, alle_Übergänge, Sij_xyz, Tau_ijk, Konzentration, step, Emin):
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        retlist = []
        Mü_ijk_add = add_arrays_with_concentration(Mü_ijk, Konzentration)
        Mü0_add = add_first_four_with_concentration(Mü0, Konzentration)
        Mü_add = np.zeros_like(Mü[0])
        for i in range(len(Mü)):
            Mü_add += Konzentration[i] * Mü[i]
        for i in range(len(Tau)):
            if (alle_Übergänge[i] == []):
                retlist.append([])
            else:
                Ubergang = [Übergänge[0] for Übergänge in alle_Übergänge[i]]
                Ubergangswhs_ijk = [Übergänge[2] for Übergänge in alle_Übergänge[i]]
                for index, ijk in enumerate(Ubergang):
                    if (ijk//100 == 91 ):
                        Kante = 0
                    elif (ijk//100 == 21 ):
                        Kante = 1
                    elif (ijk//100 == 22 ):
                         Kante = 2
                    else:
                         Kante = 3
                    dummy = Tube0[i][Kante] * Konzentration[i] * Tau0[i][Kante] * Sij0[i][Kante] * Omega0[i][Kante] * Ubergangswhs_ijk[index] / (Mü0_add[i][Kante] / cos + Mü_ijk_add[i][index] / cos) #Ltf  für diese Energie immer 1
                    for k in range(int(alle_Kanten[i][Kante] / self.step - self.Emin / self.step + 1), len(Tau[i])):
                        dummy += Countrate[k] * Konzentration[i] * Tau[i][k] * Sij[i][Kante][k - int(alle_Kanten[i][Kante] / self.step - self.Emin / self.step + 1)] * Omega0[i][Kante] * Ubergangswhs_ijk[index] / (Mü_add[k] / cos + Mü_ijk_add[i][index] / cos)
                    dummy *= Det_ijk[i][index] * const
                    retlist.append((ijk, dummy))
        return retlist

    def Intensität_K_alle(self):
        Werte = self.Werte_vorbereiten_alle(self.Probe1)
        Prim = self.Primärintensität_berechnen_alle(*Werte)


        #print(Prim)
        return Werte[11], Werte[15]

        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        counts = 0
        #for i in Prim:
           # if (i[0] in K_übergänge):
            #    counts += i[1]
                #print(i)
        return 0
    def Werte_vorbereiten(self):
        x_Element = Element(Dateipfad=self.Dateipfad, Element=self.Element_Probe, Emin = self.Emin, Emax = self.Emax, step = self.step)
        #self.Element_Probe = x_Element.Get_Elementsymbol()
        Tube0, Tau0, Omega0, Mü0, Sij0, Kantenenergie = [], [], [], [], [], []
        for i in range(4):
            Energie = x_Element.Kanten()[i][1]
            step = (int(Energie/self.step)+1)*self.step - Energie
            Tube0.append(self.Röhre.GetCountRateChar(Energie, step)+self.Röhre.GetCountRateCont(Energie, step)[0][0])
            Tau0.append(x_Element.Massenabsorptionskoeffizient(Energie)[1][0])
            Sij0.append(x_Element.S_ij(x_Element.Kanten()[i][0], Energie))
            Omega0.append(x_Element.Omega_Schale(x_Element.Kanten()[i][0]))
            Mü0.append(x_Element.Massenschwächungskoeffizient(Energie)[1][0])
            Kantenenergie.append(Energie)
        Tau = x_Element.tau
        Mü = x_Element.mü
        Ltf = x_Element.Löcherübertrag()#Lochtransferfaktor
        Countrate = self.Röhre.Countrate_gesamt
        Ubergang = [i[0] for i in x_Element.Ubergange()]
        Ubergangswhs_ijk = [Ubergang[2] for Ubergang in x_Element.Ubergange()]
        Det_ijk = [ self.Detektor.Detektoreffizienz(Ubergang[1]) for Ubergang in x_Element.Ubergange()]
        Mü_ijk = [ x_Element.Massenschwächungskoeffizient(Ubergang[1])[1][0] for Ubergang in x_Element.Ubergange()]
        Ubergangenergie = [Ubergang[1] for Ubergang in x_Element.Ubergange()]
        Tau_ijk = [ x_Element.Massenabsorptionskoeffizient(Ubergang[1])[1][0] for Ubergang in x_Element.Ubergange()]
        Sij = [0, 0, 0, 0]
        Sij_xyz = []
        for index, i in enumerate(x_Element.Kanten()[0:4]):
            Sij_Kante = [x_Element.S_ij(i[0][0:2], k * self.step) for k in range(int(i[1]/self.step + 1), round(self.Emax/self.step + 1))]
            Sij[index] = (np.array(Sij_Kante))
            Sij_xyz.append(np.array([x_Element.S_ij(i[0][0:2], Ubergang[1]) for Ubergang in x_Element.Ubergange()]))
        #print(Ltf)
        return Tube0, Tau0, Omega0, Mü0, Sij0, Tau[1], Mü[1], Countrate[1], Ubergangswhs_ijk, Mü_ijk, Det_ijk, Sij, Ubergang, Kantenenergie, Ubergangenergie, Sij_xyz, Tau_ijk, Ltf, self.step, self.Emin

    def Primärintensität_berechnen(self, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Ubergangswhs_ijk, Mü_ijk, Det_ijk, Sij, Ubergang, Kantenenergie, Ubergangenergie, Sij_xyz, Tau_ijk, Ltf, step, Emin):   #(Element, Intensität)
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        retlist = []
        for index, ijk in enumerate(Ubergang):
            if (ijk[0:2] ==" K" ):
                Kante = 0
            elif (ijk[0:2] =="L1" ):
                Kante = 1
            elif (ijk[0:2] =="L2" ):
                 Kante = 2
            else:
                 Kante = 3
            dummy = Tube0[Kante] * Tau0[Kante] * Sij0[Kante] * Omega0[Kante] * Ubergangswhs_ijk[index] / (Mü0[Kante] / cos + Mü_ijk[index] / cos) #Ltf  für diese Energie immer 1
            for k in range(int(Kantenenergie[Kante] / self.step - self.Emin / self.step + 1), len(Tau)):
                dummy += Countrate[k] * Tau[k] * Ltf[Kante+1][k] * Sij[Kante][k - int(Kantenenergie[Kante] / self.step - self.Emin / self.step + 1)] * Omega0[Kante] * Ubergangswhs_ijk[index] / (Mü[k] / cos + Mü_ijk[index] / cos)
            dummy *= Det_ijk[index] * const
            retlist.append((ijk, dummy))
        return retlist

    def Sekundärintensität_berechnen(self, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Ubergangswhs_ijk, Mü_ijk, Det_ijk, Sij, Ubergang, Kantenenergie, Ubergangenergie, Sij_xyz, Tau_ijk, Ltf, step, Emin):
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        retlist = []
        for index_ijk, ijk in enumerate(Ubergang):
            countrate = 0
            if (ijk[0:2] ==" K" ):
                Kante_ij = 0
            elif (ijk[0:2] =="L1" ):
                Kante_ij = 1
            elif (ijk[0:2] =="L2" ):
                 Kante_ij = 2
            else:
                Kante_ij = 3
            for index_xyz, xyz in enumerate(Ubergang):
                if (Kantenenergie[Kante_ij] <= Ubergangenergie[index_xyz]):
                    if (xyz[0:2] ==" K" ):
                        Kante_xy = 0
                    elif (xyz[0:2] =="L1" ):
                        Kante_xy = 1
                    elif (xyz[0:2] =="L2" ):
                        Kante_xy = 2
                    else:
                        Kante_xy = 3

                    integral = cos / Mü_ijk[index_ijk] * np.log(1 + Mü_ijk[index_ijk] / (cos * Mü_ijk[index_xyz]))
                    integral += (cos / Mü0[Kante_xy]) * np.log(1 + Mü0[Kante_xy] / (cos * Mü_ijk[index_xyz]))
                    integral *= Sij0[Kante_xy] * Tube0[Kante_xy] * Omega0[Kante_xy] * Ubergangswhs_ijk[index_xyz] * Tau0[Kante_xy] / ((Mü0[Kante_xy] / cos)+(Mü_ijk[index_ijk]/cos))
                    integralconst = cos / Mü_ijk[index_ijk] * np.log(1 + Mü_ijk[index_ijk] / (cos * Mü_ijk[index_xyz]))
                    for k in range(int(Kantenenergie[Kante_xy] / step - Emin / step + 1), len(Tau)):
                        dummy = integralconst + (cos / Mü[k] * np.log(1 + Mü[k] / (cos * Mü_ijk[index_xyz])))
                        dummy *= Sij[Kante_xy][k - int(Kantenenergie[Kante_xy] / step + Emin / step - 1)] * Tau[k] * Omega0[Kante_xy] * Ubergangswhs_ijk[index_xyz] * Countrate[k] / (Mü[k] / cos + Mü_ijk[index_ijk] / cos)
                        integral += dummy

                    integral *= const * Sij_xyz[Kante_ij][index_xyz] * Omega0[Kante_ij] * Ubergangswhs_ijk[index_ijk] * Det_ijk[index_ijk] * 0.5 * Tau_ijk[index_xyz]

                    countrate += integral
            #print(ijk, countrate )

            retlist.append((ijk, countrate))
        return retlist

 #   def Primärintensität(self):
  #      self.Primärintensität_berechnen(*self.Werte_vorbereiten())

  #  def Sekundärintensität(self):
  #      self.Sekundärintensität_berechnen(*self.Werte_vorbereiten())

    def Intensität_K(self):
        Werte = self.Werte_vorbereiten()
        Prim = self.Primärintensität_berechnen(*Werte)
        Sek = self.Sekundärintensität_berechnen(*Werte)
        #print(Sek)
        K_übergänge = [" K-L1", " K-L2", " K-L3"]
        counts = 0
        for i in Prim:
            if (i[0] in K_übergänge):
                counts += i[1]
                #print(i)
        for i in Sek:
            if (i[0] in K_übergänge):
                counts += i[1]
        return counts

    def Intensität_L(self):
        Werte = self.Werte_vorbereiten()
        Prim = self.Primärintensität_berechnen(*Werte)
        Sek = self.Sekundärintensität_berechnen(*Werte)
        L_übergänge = ["L3-M4", "L3-M5"]
        counts = 0
        for i in Prim:
            if (i[0] in L_übergänge):
                counts += i[1]
        for i in Sek:
            if (i[0] in L_übergänge):
                counts += i[1]
        return counts


    def Geometriefaktor_ati_K(self, Tupel):   #(Element, Intensität)
        x_Element = Element(Dateipfad=self.Dateipfad, Element=Tupel[0], Emin = self.Emin, Emax = self.Emax, step = self.step)
        cos = np.cos(np.pi/4)
        const = (1/cos) * 30 * 10**-2 / 4 / np.pi / 0.5**2
        #const = 0.135047447423566
        counts_K = 0
        for j in x_Element.Ubergange():
            #if (j[0][1] == "K" and j[0][3] == "L"):
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
                #print(dummy)
                for k in range(int(Energie/self.step),len(x_Element.tau[0])):
                    dummy += self.Röhre.Countrate_gesamt[1][k] * x_Element.tau[1][k] * x_Element.S_ij(j[0][0:2], x_Element.tau[0][k]) * x_Element.Omega_Schale(j[0][0:2])*j[2]/(x_Element.mü[1][k]/cos + x_Element.Massenschwächungskoeffizient(j[1])[1][0]/cos)

                    #counts += dummy * Det.Detektoreffizienz(j[1]) * const
                #if (j[0][0:2] ==" K" and j[0][3:4] == "L"):

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
                    if (j[0][0:2] =="L1" and j[0][3:5] == "M2"):
                        print(x_Element.S_ij(j[0][0:2], x_Element.tau[0][k]))
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



    def L3_M5(self):    #für reinelement
        def Prim(Palpha, Pbeta, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Mü_ijk, Det_ijk, Sij, alle_Kanten, alle_Übergänge, Sij_xyz, Tau_ijk, Konzentration, step, Emin, Ltf):
            const = (1/Palpha) * 30 * 10**-2 / 4 / np.pi / 0.5**2
            Mü_ijk_add = np.zeros_like(Mü_ijk[0])
            Mü0_add = np.zeros_like(Mü0[0])
            Mü_add = np.zeros_like(Mü[0])
            ret = np.zeros_like(alle_Übergänge)
            ret[:, :, 2] = alle_Übergänge[:, :, 1]
            retarray=[]
            for i in range(len(Konzentration)):
                Mü_ijk_add += Mü_ijk[i] * Konzentration[i]
                Mü0_add += Mü0[i] * Konzentration[i]
                Mü_add += Konzentration[i] * Mü[i]
            for i in range(len(Tau)):
                if (alle_Übergänge[i][0][0] == 0):
                    pass
                else:
                    Ubergang = [Übergänge[0] for Übergänge in alle_Übergänge[i]]
                    Ubergangswhs_ijk = [Übergänge[2] for Übergänge in alle_Übergänge[i]]
                    for index, ijk in enumerate(Ubergang):

                        if (ijk != 0):
                            if (ijk//100 == 91):
                                Kante = 0
                            elif (ijk//100 == 21):
                                Kante = 1
                            elif (ijk//100 == 22):
                                 Kante = 2
                            else:
                                 Kante = 3

                        if ijk==2335:
                            print(ijk)
                            dummy = Tube0[i][Kante] * Konzentration[i] * Tau0[i][Kante] * Sij0[i][Kante] * Omega0[i][Kante] * Ubergangswhs_ijk[index] / (Mü0_add[i][Kante] / Palpha + Mü_ijk_add[i][index] / Pbeta) #Ltf  für diese Energie immer 1
                            for k in range(int(alle_Kanten[i][Kante] / step - Emin / step + 1), len(Tau[i])):
                                retarray.append(Countrate[k] * Konzentration[i] * Tau[i][k] * Sij[i][Kante][k] * Omega0[i][Kante] * Ubergangswhs_ijk[index] * Ltf[i][Kante + 1][k] / (Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta))
                            #dummy *= Det_ijk[i][index] * const

                            #ret[i][index][0] = ijk
                            ##ret[i][index][1] = dummy
            return retarray


        Werte = self.Werte_vorbereiten_alle_jit()
        return Prim(*Werte)



