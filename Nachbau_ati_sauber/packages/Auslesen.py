import numpy as np

def Leerzeichen_entfernen(string):
    return string.replace(" ", "")

def Array_Leereintrageentfernen(array):
    return list(filter(bool, array))

def Umformen(Liste):
    try:
        float_values = [float(wert) for wert in Liste]
    except:
        print(Liste," ist kein Float")
        return Liste
    return np.array(float_values)

class Datenauslesen():
    def __init__(self, Dateipfad, Element):
        self.Daten = []
        self.Datenerstellen(Dateipfad, Element)
        self.McMaster = []
        self.McMaster_vorbereiten()
        self.Kantenarray = []
        self.Kanten_vorbereiten()

    def Datenerstellen(self, Dateipfad, Element):
        try:
            Elementname = Element[:1].capitalize() + Element[1:].lower()
        except:
            Elementname = str(Element)
        #file = open(Dateipfad,"r")
        with open(Dateipfad, "r") as file:
            Liste =[]
            #print("READ")
            for row in file:
                Liste.append(row.rstrip('\n ').rstrip(',').split(":"))
            for index, value in enumerate(Liste):
                if (value[0] == "ELEMENT SYMBOL" and Leerzeichen_entfernen(value[1]) == Elementname):
                    index_i = index
                    break
                if (value[0] == "ATOMIC NUMBER" and Leerzeichen_entfernen(value[1]) == Elementname):
                    index_i = index - 1
                    break
            for i, v in enumerate(Liste[index_i:]):
                if (v[0][0:3] =="---" ):
                    break
            self.Daten = Liste[index_i:index_i + i]

    def Get_Daten(self):
        return self.Daten
    def Get_Elementsymbol(self):
        return Leerzeichen_entfernen(self.Daten[0][1])
    def Get_Atomicnumber(self):
        return int(Leerzeichen_entfernen(self.Daten[1][1]))
    def Get_Atomicweight(self):
        return float(Leerzeichen_entfernen(self.Daten[2][1]))
    def Get_Density(self):
        return float(Leerzeichen_entfernen(self.Daten[3][1]))
    def Get_cm2g(self):
        return 0.602214179 / float(self.Get_Atomicweight())
    #McMaster Parameter K, L, M, N, coh, incoh
    def McMaster_vorbereiten(self):
        for i, v in enumerate(self.Daten):
            if (v[0][0:8] == "MCMASTER"):
                break
        McMaster = []
        Liste = []
        for i2 in range(6):
            for j in range(4):
                Liste.append(list(filter(lambda x: x != "", self.Daten[i+1:i+5][j][1].split(" ")))[i2])
            McMaster.append(Liste)
            Liste = []
        self.McMaster = [Umformen(i) for i in McMaster]
        return 0

    def Get_McMaster(self):
        return self.McMaster

    def Jumps(self):
        array = np.ones(21)
        index_i, index_j = 0, 0
        for i, v in enumerate(self.Daten):
            if (v[0] == ' K-EDGE JUMP' ):
                index_i = i
            if (v[0][0:8] == "MCMASTER"):
                index_j = i
        if (index_i == 0):
            return array
        else:
            for i in range(len(self.Daten[index_i:index_j])):
                array[i] = float(self.Daten[index_i + i][1])
            return array

    def Kanten_vorbereiten(self):
        for i, v in enumerate(self.Daten):
            if (v[0][0:3] == ' K/' ):
                index_i = i
        Jumps = self.Jumps()
        retlist = [[self.Daten[index_i + i][0].split("/")[0], float(self.Daten[index_i + i][0].split("/")[1]), Jumps[i]] for i in range(21)]
        self.Kantenarray = retlist
        return 0

    def Kanten(self):
        return self.Kantenarray
    #Name, Energie, Rate
    def Ubergange(self):
        anfang, ende1, ende2 = 0, 200, 200
        for i, v in enumerate(self.Daten):
                if (v[0][0:8] == 'SIEGBAHN' ):
                    anfang = i + 1
                if (v[0][0:7] == ' K-EDGE' ):
                    ende1 = i
                if (v[0][0:8] == "MCMASTER"):
                    ende2 = i
        if (anfang == 0):
            return [[]]
        retlist = [[self.Daten[anfang + i][0].split("/")[1], float(self.Daten[anfang + i][0].split("/")[2]), float(self.Daten[anfang + i][0].split("/")[4])] for i in range(min([ende1, ende2]) - anfang) if (float(self.Daten[anfang + i][0].split("/")[4]) != 0)]
        return retlist

    def Omega(self):
        for i, v in enumerate(self.Daten):
            if (v[0][0:7] == "Omega-K"):
                break
        Omega = []
        for neu_i in range(4):
            Omega.append(self.Daten[i + neu_i])
        return Omega
    #Schale " K", "L1", "L2", "L3"
    def Omega_Schale(self, Schale):
        Omegas = self.Omega()
        if (len(Schale.replace(" ", "")) ==1):
            return float(Omegas[0][1])
        else:
            for i in Omegas:
                if (i[0][6:] == Schale):
                    return float(i[1])

    def Costa_Kronig(self):
        return [float(i[1]) for i in self.Daten[-5:]]





#folder_path = 'C:\\Users\\julia\\OneDrive\\Dokumente' \
   #           '\\A_Christian\\Masterarbeit\\Atiquant\\BGQXRFPN\\BGQXRFPN\\MCMASTER.TXT'
#Daten = Datenauslesen(folder_path, "45")




