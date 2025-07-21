from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import  Massenschwächungskoeffizient
import numpy as np

class Element(Massenschwächungskoeffizient):
    def __init__(self, Emin = 0, Emax = 35, step = 0.05, Element = "Ag", Dateipfad = 'C:\\Users\\julia\\OneDrive\\Dokumente' \
              '\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'):
        super().__init__(Dateipfad=Dateipfad, Element=Element, Emin = Emin if Emin != 0 else step, Emax = Emax, step = step)

    def S_ij(self, Kante, Energie):
        Kante = Kante.replace(" ", "")
        SK, SL1, SL2, SL3 = self.Jumps()[0:4] #Jumps
        KK, KL1, KL2, KL3 = [Kante[1] for Kante in self.Kanten()[:4]] #Kanten
        if (Energie >= KK):
            if (Kante == "K"):
                return (SK-1)/SK
            elif (Kante == "L1"):
                return (SL1-1)/(SK*SL1)
            elif (Kante == "L2"):
                return (SL2-1)/(SK*SL1*SL2)
            elif (Kante == "L3"):
                return (SL3-1)/(SK*SL1*SL2*SL3)
        elif (Energie >= KL1):
            if (Kante == "L1"):
                return (SL1-1)/(SL1)
            elif (Kante == "L2"):
                return (SL2-1)/(SL1*SL2)
            elif (Kante == "L3"):
                return (SL3-1)/(SL1*SL2*SL3)
        elif (Energie >= KL2):
            if (Kante == "L2"):
                return (SL2-1)/(SL2)
            elif (Kante == "L3"):
                return (SL3-1)/(SL2*SL3)
        elif (Energie >= KL3):
            if(Kante == "L3"):
                return (SL3-1)/(SL3)
        return 0

    def K_gemittel_ubergang(self):
        Faktor = 0
        Ubergansenergie = 0
        for i in self.Ubergange():
            if (i[0][1] == "K" and i[0][3] == "L"):
                Ubergansenergie += i[1] * i[2]
                Faktor += i[2]
        return Ubergansenergie / Faktor

    def L_gemittel_ubergang(self):
        Faktor = 0
        Ubergansenergie = 0
        for i in self.Ubergange():
            if (i[0][0:2] == "L3" and (i[0][3:5] == "M4" or i[0][3:5] == "M5")):
                Ubergansenergie += i[1] * i[2]
                Faktor += i[2]
        return Ubergansenergie / Faktor

    def Formatumwandlung_4(self, retlist):#für 4 arrays
        Energie = [E[0] for E in retlist]
        K = [c[1] for c in retlist]
        L1 = [c[2] for c in retlist]
        L2 = [c[3] for c in retlist]
        L3 = [c[4] for c in retlist]
        #Energie.reverse()
        #K.reverse()
        #L1.reverse
        return [np.array(Energie), np.array(K), np.array(L1), np.array(L2), np.array(L3)]

    def Löcherübertrag_L3_Energie(self, Energie):
        if (Energie <= self.Kanten()[0][1] and Energie >= self.Kanten()[3][1] and self.Get_Atomicnumber()>=28):   #erst ab 28 gibt es L1,L2,L3 Jumps
            #print(self.S_ij("L2", Energie),self.S_ij("L3", Energie))
            retval = 1 + self.S_ij("L2", Energie) / self.S_ij("L3", Energie) * self.Costa_Kronig()[4] + \
            self.S_ij("L1", Energie) / self.S_ij("L3", Energie) * \
                     (self.Costa_Kronig()[2] + self.Costa_Kronig()[3] + self.Costa_Kronig()[1] * self.Costa_Kronig()[4])
            return retval
        else:
            return 1

    def Löcherübertrag_L2_Energie(self, Energie):
        if (Energie <= self.Kanten()[0][1] and Energie >= self.Kanten()[2][1] and self.Get_Atomicnumber()>=28):
            retval = 1 + self.S_ij("L1", Energie) / self.S_ij("L2", Energie) * self.Costa_Kronig()[1]
            return retval
        else:
            return 1

    def Löcherübertrag(self):
        #for i in np.arange(self.Emin,self.Emax,self.step):
        #Arraylänge = round((self.Emax - self.Emin ) / self.step) + 1
        retlist = []
        #for i in range(Arraylänge):
        for Energie in np.arange(self.Emin,self.Emax+self.step,self.step):
            retlist.append([Energie, 1, 1, self.Löcherübertrag_L2_Energie(Energie), self.Löcherübertrag_L3_Energie(Energie)])
        return self.Formatumwandlung_4(retlist)









