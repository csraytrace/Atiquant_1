#from packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
import matplotlib.pyplot as plt
import numpy as np

#folder_path = 'C:\\Users\\julia\\OneDrive\\Dokumente' \
#              '\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'
#Daten = Datenauslesen(folder_path, "90")
def BeerLambert(Massenschwachungskoe, Dichte, Dicke, Phi = 0):
    return np.exp(-Massenschwachungskoe * Dichte * Dicke / np.cos(Phi * np.pi / 180))

class Detektor():
    def __init__(self, Fenstermaterial = "Be", Fensterdicke = 7.62, phi = 0, Kontakmaterial = "Au", Kontaktmaterialdicke = 50,
                 Bedeckungsfaktor = 1, Detektormaterial = "Si", Totschicht = 0.05, activeLayer = 3,
                 Dateipfad = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT',
                 Emin = 0, Emax = 35, step = 0.05):
        """Initialisiert eines Detektor:
        mit 3 verschiedenen Materialen (Fenster-, Kontaktschicht und Detektormaterial)
        einem einfalldem Winkel phi
        Fensterdicke in Mikrometern
        Kontaktmaterialdicke in Nanometern
        und den Detektorschichten Totschicht in Mikrometern und activeLayer in Milimetern, Dateipfad für Elemente und Energiebereich mit Schrittgröße für ein Detektorspektrum"""
        self.Fenstermaterial = Fenstermaterial
        self.Fensterdicke = Fensterdicke * 1e-4
        self.phi = phi
        self.Kontaktmaterial = Kontakmaterial
        self.Kontaktmaterialdicke = Kontaktmaterialdicke * 1e-7
        self.Bedeckungsfaktor = Bedeckungsfaktor
        self.Detektormaterial = Detektormaterial
        self.Totschicht = Totschicht * 1e-4
        self.activeLayer = activeLayer * 1e-1
        self.folder_path = Dateipfad
        self.Emin = Emin if Emin != 0 else step
        self.Emax = Emax
        self.step = step
        self.Mü_Kontaktmaterial = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element= self.Kontaktmaterial, Dateipfad=self.folder_path)
        self.Mü_Fenstermaterial = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element= self.Fenstermaterial, Dateipfad=self.folder_path)
        self.Mü_Detektor = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Detektormaterial, Dateipfad=self.folder_path)
        #self.Massenschwächungskoeffizientenberechnung()

    #def Massenschwächungskoeffizientenberechnung(self):
    #    self.Mü_Fenstermaterial = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element= self.Fenstermaterial, Dateipfad=self.folder_path)
    #    self.Mü_Kontaktmaterial = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element= self.Kontaktmaterial, Dateipfad=self.folder_path)
    #    self.Mü_Detektor = Massenschwächungskoeffizient(Emin=self.Emin, Emax=self.Emax, step=self.step, Element=self.Detektormaterial, Dateipfad=self.folder_path)

    def Detektoreffizienz(self, Energie):
        effizienz = BeerLambert(self.Mü_Fenstermaterial.Massenschwächungskoeffizient(Energie)[1], float(self.Mü_Fenstermaterial.Get_Density()), self.Fensterdicke)
        effizienz *= BeerLambert(self.Mü_Detektor.Massenschwächungskoeffizient(Energie)[1], float(self.Mü_Detektor.Get_Density()), self.Totschicht)
        effizienz *= 1-self.Bedeckungsfaktor + self.Bedeckungsfaktor * BeerLambert(self.Mü_Kontaktmaterial.Massenschwächungskoeffizient(Energie)[1], float(self.Mü_Kontaktmaterial.Get_Density()), self.Kontaktmaterialdicke)
        effizienz *= 1 - BeerLambert(self.Mü_Detektor.Massenschwächungskoeffizient(Energie)[1], float(self.Mü_Detektor.Get_Density()), self.activeLayer)
        return effizienz[0]


    def Detektorspektrum(self):
        Detektoreffizienz = []
        Mü_Fenster = self.Mü_Fenstermaterial.mü[1]
        Fensterdichte = float(self.Mü_Fenstermaterial.Get_Density())
        Mü_Kontakt = self.Mü_Kontaktmaterial.mü[1]
        Kontaktdichte = float(self.Mü_Kontaktmaterial.Get_Density())
        Mü_Detektor = self.Mü_Detektor.mü[1]
        Detektordichte = float(self.Mü_Detektor.Get_Density())

        for i in range(len(Mü_Fenster)):
            effizienz = BeerLambert(Mü_Fenster[i], Fensterdichte, self.Fensterdicke)
            effizienz *= BeerLambert(Mü_Detektor[i], Detektordichte, self.Totschicht)
            effizienz *= 1-self.Bedeckungsfaktor + self.Bedeckungsfaktor * BeerLambert(Mü_Kontakt[i], Kontaktdichte, self.Kontaktmaterialdicke)
            effizienz *= 1 - BeerLambert(Mü_Detektor[i], Detektordichte, self.activeLayer)
            Detektoreffizienz.append(effizienz)
        return [self.Mü_Fenstermaterial.Massenschwächungskoeffizient_array()[0], np.array(Detektoreffizienz)]


#dec = Detektor()
#dec.Detektorspektrum()
