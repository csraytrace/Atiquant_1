from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
import numpy as np
import copy
def BeerLambert(Massenschwachungskoe, Dichte, Dicke, Fenstereinfallwinkel):
    return np.exp(-Massenschwachungskoe * Dichte * Dicke / Fenstereinfallwinkel)
class Röhre():
    def __init__(self, Röhrenmaterial = "Rh", Einfallswinkelalpha = 20, Einfallswinkelbeta = 70, Fensterwinkel = 0, charzucont = 1,charzucont_L=1,
                Fenstermaterial = "Be", Fensterdicke = 125, Raumwinkel = 1, Röhrenstrom = 0.01, Emin = 0, Emax = 35, sigma = 1.0314,
                step=0.05, Messzeit = 30, folder_path='C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'):
        self.Röhrenmaterial = Röhrenmaterial
        self.Einfallwinkelalpha = np.cos(np.pi / 180 * Einfallswinkelalpha)
        self.Einfallwinkelbeta = np.cos(np.pi / 180 * Einfallswinkelbeta)
        self.Fenstereinfallwinkel = np.cos(np.pi / 180 * Fensterwinkel) #brauch?
        self.Fenstermaterial = Fenstermaterial
        self.Fensterdicke = Fensterdicke * 1e-4
        self.Raumwinkel = Raumwinkel
        self.Röhrenstrom = Röhrenstrom
        self.Emin = Emin if Emin != 0 else step
        self.Emax = Emax  #== die Röhrenspannung auch wenn Einheit nicht passt
        self.sigma = sigma
        self.step = step
        self.Messzeit = Messzeit
        self.folder_path = folder_path
        self.Eindringtiefe_zähler = 0 #ohne ln
        self.Eindringtiefe_nenner = 0 #ohne ln
        self.x = 0
        self.Daten_Anode = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Röhrenmaterial, Dateipfad=self.folder_path)
        self.Daten_Fenster = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Fenstermaterial, Dateipfad=self.folder_path)
        self.Röhrenspektrum = [[],[]]
        #self.Röhrenspektrum_ohne_Fenster = [[],[]]
        self.charzucont = charzucont
        self.charzucont_L = charzucont_L
        self.Char_spec = []
        self.Countrate_gesamt = [[],[]]
        self.Gesamtspektrum_plot = [[],[]]
        self.Werte_vorbereiten()

    def Werte_vorbereiten(self):
        #self.Daten_Anode = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Röhrenmaterial, folder_path=self.folder_path)
        #self.Daten_Fenster = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Fenstermaterial, folder_path=self.folder_path)
        weight = self.Daten_Anode.Get_Atomicweight()/self.Daten_Anode.Get_Density()
        Z = self.Daten_Anode.Get_Atomicnumber()
        J = Z * 0.0135
        maxpenetrationdepth = weight/Z*(0.787e-5*np.sqrt(J)*self.Emax**(3/2)+0.735e-6*self.Emax**2)
        m = 0.1382-(0.9211/np.sqrt(Z))
        lnZ = np.log(Z)
        n = self.Emax**m * (0.1904-0.2236*lnZ+0.1292*lnZ**2-0.01491*lnZ**3)
        self.Eindringtiefe_zähler = maxpenetrationdepth*(0.49269-1.0987*n+0.78557*n**2) #ohne E_abhängigkeit
        self.Eindringtiefe_nenner = 0.70256-1.09865*n+1.0046*n**2
        self.x = 1.0314-0.0032*Z+0.0047*self.Emax
        self.Röhrenspektrum_cont_berechnen()
        self.Charstrahlung_berechnen()
        self.Gesamtspektrumcountrate_berechnen()


    def Röhrenspektrum_cont_berechnen(self):
        Anoden_Tau = self.Daten_Anode.tau
        Fenster_Mü = self.Daten_Fenster.mü
        Dichte_Fenster = self.Daten_Fenster.Get_Density()
        retlist = []
        nach_Fenster = []
        Z = self.Daten_Anode.Get_Atomicnumber()
        D = self.Daten_Anode.Get_Density()
        for i, E in enumerate(Anoden_Tau[0]):
            U = self.Emax/E
            lnU = np.log(U)
            z_quer = self.Eindringtiefe_zähler * lnU / (self.Eindringtiefe_nenner + lnU)

            #sigma = 1.36e9 * Z * (U-1)**(self.sigma[0]-self.sigma[1]*Z + self.sigma[2] * self.Emax)
            sigma = 1.36e9 * Z * (U-1)**(self.sigma-0.0032*Z + 0.0047 * self.Emax)
            #sigma = 1.35e9 * Z * (U-1)**(1.109-0.00435*Z + 0.00175 * Emax) #loveScott
            #sigma = 1.3844 * 10**9 * Z * (U-1)**(1.05629-0.003492*Z)#Wiederschwinger 1990

            Xi = Anoden_Tau[1][i] * self.Einfallwinkelalpha / self.Einfallwinkelbeta
            if (Xi == 0 or z_quer == 0):
                fx = 0
            else:
                fx = (1 - np.exp((-2) * Xi * D * z_quer))/(2 * Xi * D * z_quer)

            Photonenanzahl = sigma * fx * self.Röhrenstrom * self.Messzeit * self.step * self.Raumwinkel * BeerLambert(Fenster_Mü[1][i], Dichte_Fenster, self.Fensterdicke, self.Fenstereinfallwinkel)#* 1/self.step  #1/step damit keine bins entstehen
            if(Photonenanzahl>1 and E>0.2):
                threshold = 1
            else:
                threshold = 0

            #retlist.append(Photonenanzahl*trashold)
            nach_Fenster.append(Photonenanzahl * threshold)
        self.Röhrenspektrum = [Anoden_Tau[0], np.array(nach_Fenster)]
        #self.Röhrenspektrum_ohne_Fenster = [Anoden_Tau[0], np.array(retlist)]
        #return [Anoden_Tau[0], np.array(retlist)]
        return 0

    #def Röhrenspektrum_cont(self):
      #  return self.Röhrenspektrum

    #def Röhrenspektrum_cont_ohne_Fenster(self):
     #   return self.Röhrenspektrum_ohne_Fenster

    def Charstrahlung_berechnen(self):
        Char_spec = []
        Emax = self.Emax
        Z = self.Daten_Anode.Get_Atomicnumber()
        D = self.Daten_Anode.Get_Density()
        J = 0.0135 * Z
        Ubergange = self.Daten_Anode.Ubergange()
        Omega = self.Daten_Anode.Omega()
        Kanten = self.Daten_Anode.Kanten()
        a = [[5.580848699E-3,2.709177328E-4,-5.531081141E-6,5.95579625E-8,-3.210316856E-10],
            [3.401533559E-2,-1.601761397E-4,2.473523226E-6,-3.020861042E-8,0.0],[9.916651666E-2,-4.615018255E-4,-4.332933627E-7,0.0,0.0],
            [1.030099792E-1,-3.113053618E-4,0.0,0.0,0.0],[3.630169747E-2,0.0,0.0,0.0,0.0]]
        a = np.array(a)
        #Parameter gibt S-Energie, U-Energie, Omega, z und b und überganswahrscheinlichkeit zurück
        def Parameter(Ubergang_i, Omega, Kanten):
            if (Ubergang_i[0][:2].replace(" ", "") == Omega[0][0][6:8].replace(" ", "")):
                #K-Übergang
                return Kanten[0][1],Ubergang_i[1],float((Omega[0][1])),2, 0.35, Ubergang_i[2]
            else:
                for i in Omega[1:]:
                    if (Ubergang_i[0][:2] == i[0][6:8]):
                        for j in Kanten:
                            if(Ubergang_i[0][:2] == j[0]):
                                #L_übergänge
                                return j[1],Ubergang_i[1],float((i[1])),8, 0.25, Ubergang_i[2]
        for Ubergang_einzel in Ubergange:
            S_Energie, U_Energie, Omega_einzel, z, b, p_jk = Parameter(Ubergang_einzel, Omega, Kanten)#U_Energie = Ubergangsenergie, S=Schalenenergie
            #print(Ubergang_einzel, S_Energie, U_Energie, Omega_einzel, z, b)
            U = self.Emax / S_Energie
            lnU = np.log(U)
            Klammer = 1 + 16.05 * np.sqrt(J/S_Energie) * (np.sqrt(U) * lnU + 2 * (1 - np.sqrt(U))) / (U * lnU + 1 - U)
            Intensitatsfaktor = z * b / Z * (U * lnU +1-U) * Klammer

            R = 1
            for y in range(0, 5):
                for x in range(0, y+1):
                    R += a[x, y-x] * (1 / U - 1)**(x+1) * Z**(y-x+1)
            if (U_Energie==0):
                Char_spec.append([U_Energie,0,Ubergang_einzel[0]])
            else:
                #für die Übergangsenergie
                U = Emax / U_Energie
                lnU = np.log(U)
                z_quer = self.Eindringtiefe_zähler * lnU / (self.Eindringtiefe_nenner + lnU)
                Tau_anode = self.Daten_Anode.Massenabsorptionskoeffizient(U_Energie)[1]
                Mü_Fenster = self.Daten_Fenster.Massenschwächungskoeffizient(U_Energie)[1][0]
                Dichte_Fenster = self.Daten_Fenster.Get_Density()

                Xi = Tau_anode * self.Einfallwinkelalpha / self.Einfallwinkelbeta
                if (Xi == 0 or z_quer == 0):
                    fx = 0
                else:
                    fx = (1 - np.exp((-2) * Xi * D * z_quer))/(2 * Xi * D * z_quer)
                if (self.Emax > U_Energie):
                    Char_spec.append([U_Energie, (self.charzucont*6*10**13*Intensitatsfaktor*R*p_jk*fx*Omega_einzel*self.Röhrenstrom*BeerLambert(Mü_Fenster, Dichte_Fenster, self.Fensterdicke, self.Fenstereinfallwinkel))[0]*self.Messzeit,Ubergang_einzel[0]])
        for index, i in enumerate(Char_spec):
            if (i[2][0:1]=="L"):
                Char_spec[index][1] *= self.charzucont_L
        self.Char_spec = Char_spec

        return Char_spec

    #def Charstrahlung(self):
    #    return self.Char_spec

    #def Countrate_spektrum(self):
    #    return self.Countrate_gesamt

    #absorb Chi, Chi, Tau  -->Photonenzahl nach Röhre, Photonenzahl ohne Fensterabsorption, Tau
    def GetCountRateCont(self, Energie, step = None):
        if step is None:
            step = self.step
        Anoden_Tau = self.Daten_Anode.Massenabsorptionskoeffizient(Energie)[1]
        if (self.Emax <= Energie):
            return (np.zeros(1), np.zeros(1), Anoden_Tau)
        if (Energie+self.step > self.Emax):
            step = self.Emax - Energie
        Fenster_Mü = self.Daten_Fenster.Massenschwächungskoeffizient(Energie)[1]
        Dichte_Fenster = self.Daten_Fenster.Get_Density()
        Z = self.Daten_Anode.Get_Atomicnumber()
        D = self.Daten_Anode.Get_Density()
        U = self.Emax/Energie
        lnU = np.log(U)
        z_quer = self.Eindringtiefe_zähler * lnU / (self.Eindringtiefe_nenner + lnU)
        sigma = 1.36e9 * Z * (U-1)**(1.0314-0.0032*Z + 0.0047 * self.Emax)
        Xi = Anoden_Tau * self.Einfallwinkelalpha / self.Einfallwinkelbeta
        if (Xi == 0 or z_quer == 0):
            fx = 0
        else:
            fx = (1 - np.exp((-2) * Xi * D * z_quer))/(2 * Xi * D * z_quer)
        Photonenanzahl = sigma * fx * self.Röhrenstrom * self.Messzeit * step * self.Raumwinkel# * 1/step  #1/step damit keine bins entstehen


        return (Photonenanzahl * BeerLambert(Fenster_Mü, Dichte_Fenster, self.Fensterdicke, self.Fenstereinfallwinkel), Photonenanzahl, Anoden_Tau)

    def GetCountRateChar(self, Energie, step = None):
        if step is None:
            step = self.step
        Spektrum = self.Char_spec
        summe = 0
        for i in range(len(Spektrum)):
            if (Energie <= Spektrum[i][0] and Energie + step > Spektrum[i][0]):
                summe += Spektrum[i][1]
        return summe

    def Gesamtspektrumcountrate_berechnen(self):
        #Spektrum = self.Röhrenspektrum_cont().copy()
        Spektrum = copy.deepcopy(self.Röhrenspektrum)
        Spektrum_plot = copy.deepcopy(self.Röhrenspektrum)
        Spektrum_plot[1] /= self.step
        for x in self.Char_spec:
            if (x[0] < self.Emax and x[1] > 1 and x[0] > self.Emin):
                Index = int((x[0] - self.Emin)/self.step)
                Spektrum[1][Index] += x[1]
                Spektrum_plot[1][Index] += x[1]
        self.Countrate_gesamt = Spektrum
        self.Gesamtspektrum_plot = Spektrum_plot





