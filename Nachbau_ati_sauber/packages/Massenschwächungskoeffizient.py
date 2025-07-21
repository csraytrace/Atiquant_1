from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
import numpy as np
import matplotlib.pyplot as plt
from numba import jit

@jit(nopython=True, cache=True)
def Tau_Schale_Energie_berechnen(McMasterparameter, Energie):
    summe = 0
    for i in range(len(McMasterparameter)):
        summe += McMasterparameter[i] * (np.log(Energie))**i
    return np.exp(summe)

class Massenschwächungskoeffizient(Datenauslesen):

        def __init__(self, Emin = 0, Emax = 35, step = 0.05, Element = "Cu"
                    ,Dateipfad = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT',):
            super().__init__(Dateipfad = Dateipfad, Element = Element)
            self.Emin = Emin
            self.Emax = Emax
            self.step = step
            #self.Daten = Datenauslesen(folder_path, Element)
            self.mü = []
            self.tau = []
            self.Emin_check()   #weil bei E = 0 Probleme mit McMaster kommen und niedrige Energien nicht relevant sind
            self.prepare()


        #def Get_Daten(self):
           # pass
            #return self.Daten
        def prepare(self):
            self.Massenschwächungskoeffizient_array()
            self.Massenabsorptionskoeffizient_array()
            return 0

        def Emin_check(self):
            if (self.Emin == 0):
                self.Emin += self.step
       # def Tau_Schale_Energie(self, McMasterparameter, Energie):
       #     summe = 0
        #    for i in range(len(McMasterparameter)):
        #        summe += McMasterparameter[i] * (np.log(Energie))**i
           # return np.exp(summe)
        def Tau_Schale_Energie(self, McMasterparameter, Energie):
            return Tau_Schale_Energie_berechnen(McMasterparameter, Energie)



        def TauK(self,Energie):
            return Tau_Schale_Energie_berechnen(self.Get_McMaster()[0], Energie) * self.Get_cm2g()

        def TauL(self, Energie):
            return Tau_Schale_Energie_berechnen(self.Get_McMaster()[1], Energie) * self.Get_cm2g()

        def TauM(self, Energie):
            return Tau_Schale_Energie_berechnen(self.Get_McMaster()[2], Energie) * self.Get_cm2g()

        def TauN(self, Energie):
            return Tau_Schale_Energie_berechnen(self.Get_McMaster()[3], Energie) * self.Get_cm2g()




        def Massenabsorptionskoeffizient_array(self): #Tau
            Arraylänge = round((self.Emax - self.Emin ) / self.step) + 1
            retlist = []
            for i in range(Arraylänge):
                Energie = self.Emax - i * self.step
                if (Energie >= self.Kanten()[0][1]):
                    retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[0], Energie) * self.Jump(" ", Energie)])
                elif (Energie >= self.Kanten()[3][1]):
                    retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[1], Energie) * self.Jump("L", Energie)])
                elif (Energie >= self.Kanten()[8][1]):
                    retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[2], Energie) * self.Jump("M", Energie)])
                else:
                    if (np.all(self.Get_McMaster()[3] == 0)):
                        retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[2], Energie) * self.Jump("M", Energie)])
                    else:
                        retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[3], Energie) * self.Jump("N", Energie)])
            self.tau = self.Formatumwandlung(retlist)
            return self.Formatumwandlung(retlist)

        def Tau_coh(self):
            Arraylänge = round((self.Emax - self.Emin ) / self.step) + 1
            retlist = []
            for i in range(Arraylänge):
                Energie = self.Emax - i * self.step
                retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[4], Energie)])
            return self.Formatumwandlung(retlist)

        def Tau_incoh(self):
            Arraylänge = round((self.Emax - self.Emin ) / self.step) + 1
            retlist = []
            for i in range(Arraylänge):
                Energie = self.Emax - i * self.step
                retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[5], Energie)])
            return self.Formatumwandlung(retlist)

        def Massenschwächungskoeffizient_array(self):#mü
            self.mü = [self.Tau_coh()[0], self.Massenabsorptionskoeffizient_array()[1] + self.Tau_coh()[1] + self.Tau_incoh()[1]]
            return [self.Tau_coh()[0], self.Massenabsorptionskoeffizient_array()[1] + self.Tau_coh()[1] + self.Tau_incoh()[1]]

        def Jump(self, Kante, Energie):
            Jump = 1
            for i in (self.Kanten()):
                if (i[0][0] == Kante):
                    if (Energie < i[1]):
                        Jump *= i[2]
            return 1/Jump

        def Formatumwandlung(self, retlist):
            Energie = [E[0] for E in retlist]
            cm2g = [c[1] for c in retlist]  #cm^2/g einheit Massenschwächungskoeffizient
            Energie.reverse()
            cm2g.reverse()
            return [np.array(Energie), np.array(cm2g)]

        def Massenabsorptionskoeffizient(self, Energie): #Tau
            retlist = []
            if (Energie >= self.Kanten()[0][1]):
                retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[0], Energie) * self.Jump(" ", Energie)])
            elif (Energie >= self.Kanten()[3][1]):
                retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[1], Energie) * self.Jump("L", Energie)])
            elif (Energie >= self.Kanten()[8][1]):
                retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[2], Energie) * self.Jump("M", Energie)])
            else:
                if (np.all(self.Get_McMaster()[3] == 0)):
                    retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[2], Energie) * self.Jump("M", Energie)])
                else:
                    retlist.append([Energie, self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[3], Energie) * self.Jump("N", Energie)])
            return self.Formatumwandlung(retlist)

        def Massenschwächungskoeffizient(self, Energie): #mü
            array = self.Massenabsorptionskoeffizient(Energie)
            array[1] +=  self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[4], Energie)#kohärent
            array[1] +=  self.Get_cm2g() * self.Tau_Schale_Energie(self.Get_McMaster()[5], Energie)#inkohärent
            return array



