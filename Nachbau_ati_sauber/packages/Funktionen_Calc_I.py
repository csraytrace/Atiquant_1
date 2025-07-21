from numba import njit
import numpy as np
from Nachbau_ati_sauber.Element import Element
import re

@njit
def Primärintensität_berechnen_alle_jit(Palpha, Pbeta, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Mü_ijk, Det_ijk, Sij, alle_Kanten, alle_Übergänge, Sij_xyz, Tau_ijk, Konzentration, step, Emin, Ltf):
    const = (1/Palpha) * 30 * 10**-2 / 4 / np.pi / 0.5**2
    Mü_ijk_add = np.zeros_like(Mü_ijk[0])
    Mü0_add = np.zeros_like(Mü0[0])
    Mü_add = np.zeros_like(Mü[0])
    ret = np.zeros_like(alle_Übergänge)
    ret[:, :, 2] = alle_Übergänge[:, :, 1]
    for i in range(len(Konzentration)):
        Mü_ijk_add += Mü_ijk[i] * Konzentration[i]
        Mü0_add += Mü0[i] * Konzentration[i]
        Mü_add += Konzentration[i] * Mü[i]
    for i in range(len(Tau)):
        if (alle_Übergänge[i][0][0] == 0):
            #print("keine Übergänge")
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
                    dummy = Tube0[i][Kante] * Konzentration[i] * Tau0[i][Kante] * Sij0[i][Kante] * Omega0[i][Kante] * Ubergangswhs_ijk[index] / (Mü0_add[i][Kante] / Palpha + Mü_ijk_add[i][index] / Pbeta) #Ltf  für diese Energie immer 1
                    for k in range(int(alle_Kanten[i][Kante] / step - Emin / step + 1), len(Tau[i])):
                        dummy += Countrate[k] * Konzentration[i] * Tau[i][k] * Sij[i][Kante][k] * Omega0[i][Kante] * Ubergangswhs_ijk[index] * Ltf[i][Kante + 1][k] / (Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta)
                        #if (ijk // 100==91 and ijk % 100 == 33):
                            #print("K_M3")

                            #print(Countrate[k] * Konzentration[i] * Tau[i][k] * Sij[i][Kante][k] * Omega0[i][Kante] * Ubergangswhs_ijk[index] * Ltf[i][Kante + 1][k] / (Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta))
                            #print(("Nenner",Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta))

                        #if (ijk // 100==91 and ijk % 100 == 22):
                            #print("K_L2")

                            #print(Countrate[k] * Konzentration[i] * Tau[i][k] * Sij[i][Kante][k] * Omega0[i][Kante] * Ubergangswhs_ijk[index] * Ltf[i][Kante + 1][k] / (Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta))
                            #print(("Nenner",Mü_add[k] / Palpha + Mü_ijk_add[i][index] / Pbeta))
                            #print("sij",Sij[i][Kante][k])
                            #print("massen/absor",Mü_add[k]/Tau[i][k]/1.0154338220283299)
                            #print("count",Countrate[k])


                    dummy *= Det_ijk[i][index] * const

                    ret[i][index][0] = ijk
                    ret[i][index][1] = dummy
    return ret
@njit
def Sekundärintensität_berechnen_jit(Palpha, Pbeta, Tube0, Tau0, Omega0, Mü0, Sij0, Tau, Mü, Countrate, Mü_ijk, Det_ijk, Sij, alle_Kanten, alle_Übergänge, Sij_xyz, Tau_ijk, Konzentration, step, Emin, Ltf):
    const = (1/Palpha) * 30 * 10**-2 / 4 / np.pi / 0.5**2
    ret = np.zeros_like(alle_Übergänge)
    Mü_ijk_add = np.zeros_like(Mü_ijk[0])
    Mü0_add = np.zeros_like(Mü0[0])
    Mü_add = np.zeros_like(Mü[0])
    for i in range(len(Konzentration)):
        Mü_ijk_add += Mü_ijk[i] * Konzentration[i]
        Mü0_add += Mü0[i] * Konzentration[i]
        Mü_add += Konzentration[i] * Mü[i]
    for i in range(len(Tau)):   #Länge der Elementliste
        if (alle_Übergänge[i][0][0] == 0):
            #print("keine Übergänge")
            pass
        else:
            Ubergang_ijk = [Übergänge[0] for Übergänge in alle_Übergänge[i]]
            Ubergangswhs_ijk = [Übergänge[2] for Übergänge in alle_Übergänge[i]]
            for index_ijk, ijk in enumerate(Ubergang_ijk):
                countrate = 0
                if (ijk != 0):
                    if (ijk//100 == 91 ):
                        Kante_ij = 0
                    elif (ijk//100 == 21 ):
                        Kante_ij = 1
                    elif (ijk//100 == 22 ):
                         Kante_ij = 2
                    else:
                         Kante_ij = 3
                    for j in range(len(Tau)):
                        if (alle_Übergänge[j][0][0] == 0):
                            pass
                        else:        #  and (alle_Kanten[i][Kante_ij] <= )  if (Kantenenergie[Kante_ij] <= Ubergangenergie[index_xyz]):
                            Ubergang_xyz = [Übergänge[0] for Übergänge in alle_Übergänge[j]]
                            Ubergangsenergie_xyz = [Übergänge[1] for Übergänge in alle_Übergänge[j]]
                            Ubergangswhs_xyz = [Übergänge[2] for Übergänge in alle_Übergänge[j]]
                            for index_xyz, xyz in enumerate(Ubergang_xyz):
                                if (xyz != 0 and (alle_Kanten[i][Kante_ij] < Ubergangsenergie_xyz[index_xyz])):
                                    if (xyz//100 == 91 ):
                                        Kante_xy = 0
                                    elif (xyz//100 == 21 ):
                                        Kante_xy = 1
                                    elif (xyz//100 == 22 ):
                                         Kante_xy = 2
                                    else:
                                         Kante_xy = 3
                                    integral = Pbeta / Mü_ijk_add[i][index_ijk] * np.log(1 + Mü_ijk_add[i][index_ijk] / (Pbeta * Mü_ijk_add[j][index_xyz]))
                                    integral += (Palpha / Mü0_add[j][Kante_xy]) * np.log(1 + Mü0_add[j][Kante_xy] / (Palpha * Mü_ijk_add[j][index_xyz]))
                                    integral *= Sij0[j][Kante_xy] * Tube0[j][Kante_xy] * Omega0[j][Kante_xy] * Ubergangswhs_xyz[index_xyz] * Tau0[j][Kante_xy] / ((Mü0_add[j][Kante_xy] / Palpha)+(Mü_ijk_add[i][index_ijk]/Pbeta))#Ltf für diese Energie immer 1
                                    integralconst = Pbeta / Mü_ijk_add[i][index_ijk] * np.log(1 + Mü_ijk_add[i][index_ijk] / (Pbeta * Mü_ijk_add[j][index_xyz]))
                                    #print(Ubergangsenergie_xyz[index_xyz])

                                    for k in range(int(alle_Kanten[j][Kante_xy] / step - Emin / step + 1), len(Tau[j])):
                                        dummy = integralconst + (Palpha / Mü_add[k] * np.log(1 + Mü_add[k] / (Palpha * Mü_ijk_add[j][index_xyz])))
                                        dummy *= Sij[j][Kante_xy][k] * Tau[j][k] * Ltf[j][Kante_xy + 1][k] * Omega0[j][Kante_xy] * Ubergangswhs_xyz[index_xyz] * Countrate[k] / (Mü_add[k] / Palpha + Mü_ijk_add[i][index_ijk] / Pbeta)
                                        integral += dummy

                                    integral *= const * Sij_xyz[i][Kante_ij][index_xyz + j * len(Ubergang_xyz)] * Omega0[i][Kante_ij] * Ubergangswhs_ijk[index_ijk] * Det_ijk[i][index_ijk] * 0.5 * Tau_ijk[i][j][index_xyz] * Konzentration[i] * Konzentration[j]
                                    Übergangsenergie_xyz_index = int(Ubergangsenergie_xyz[index_xyz] / step - Emin / step + 1)
                                    integral *= Ltf[i][Kante_ij + 1][Übergangsenergie_xyz_index]
                                    #print(Ltf[i][Kante_ij + 1][Übergangsenergie_xyz_index],Übergangsenergie_xyz_index)

                                    #print(Ltf[i][Kante_ij + 1][Übergangsenergie_xyz_index],Übergangsenergie_xyz_index)
                                    #print("term", Sij_xyz[i][Kante_ij][index_xyz + j * len(Ubergang_xyz)] , Omega0[i][Kante_ij] , Ubergangswhs_ijk[index_ijk] , Det_ijk[i][index_ijk])
                                    countrate += integral
                    ret[i][index_ijk][0] = ijk
                    ret[i][index_ijk][1] = countrate

    return ret

def Probeneingabe(Probe):
    if (isinstance(Probe, int)):
        return [Probe]
    if (isinstance(Probe, list)):
        return Probe
    try:
        Länge = len(Probe)
    except:
        print("Probe nicht richtig beschrieben")
    if (Länge <=2) and isinstance(Probe, str):
        return [Probe]
    if (isinstance(Probe, tuple)):
        return [i for i in Probe]


def Verbindung_einlesen(Verbindung):#Elemente und deren Konzentration in Gewichtsprozent, Verbindung ca1c1o3 (calciumcarbonat), sonst Element Konzentration... h 1 he 2 be 1.4, die aber schon in Gewichtsprozent #wird normiert
    if " " in Verbindung:
        Konzentrationen = np.array(Verbindung.split(" ")[1::2]).astype(float)
        Konzentrationen = np.array([con / Konzentrationen.sum() for con in Konzentrationen])
        return Verbindung.split(" ")[0::2], Konzentrationen
    elif (len(Verbindung)<=2):
        if len(Verbindung) > 1 and Verbindung[1].isdigit():
            return [Verbindung[0]], np.array([1.0])
        return [Verbindung], np.array([1.0])
    else:
        pattern = r'[a-zA-Z]+|\d+'
        result = [int(item) if item.isdigit() else item for item in re.findall(pattern, Verbindung)]
        Elemente = result[0::2]
        Atomzahl = np.array(result[1::2]).astype(float)
        Element_fkt = []
        for e in Elemente:
            Element_fkt.append(Element(Element=e))
        Gesamtgewicht = 0
        for index, x in enumerate(Element_fkt):
            Gesamtgewicht += x.Get_Atomicweight() * Atomzahl[index]
    return Elemente, np.array([mas.Get_Atomicweight() * Atomzahl[index_j] / Gesamtgewicht for index_j, mas in enumerate(Element_fkt)])

def Verbindungen_Gewichtsprozent(Verbindungen): #Verbindung in Atomprozent
    Verbindung = Verbindungen.split("+")
    pattern = r'[a-zA-Z]+|\d+\.\d+e[+-]?\d+|\d+e[+-]?\d+|\d+\.\d+|\d+'
    Verbindung_konz = []
    Elemente_anzahl = []
    Elemente_fkt = []
    Elemente = []
    Ele_konz = []
    for i in range(len(Verbindung)):
        result = [float(item) if re.match(r'^\d+\.?\d*(e[+-]?\d+)?$', item) else item for item in re.findall(pattern, Verbindung[i])]
        Verbindung_konz.append(result.pop(0))
        Elemente_anzahl.append(np.array(result[1::2]).astype(float))
        Elemente_fkt.append([Element(Element=e) for e in result[0::2]])

    Gesamtgewicht = 0
    for i in range(len(Verbindung_konz)):
        for j in range(len(Elemente_anzahl[i])):
            Gesamtgewicht += Verbindung_konz[i] * Elemente_fkt[i][j].Get_Atomicweight() * Elemente_anzahl[i][j]
    for i in range(len(Verbindung_konz)):
        for j in range(len(Elemente_anzahl[i])):
            Symbol = Elemente_fkt[i][j].Get_Elementsymbol()
            if Symbol in Elemente:
                Ele_konz[Elemente.index(Symbol)] += Elemente_fkt[i][j].Get_Atomicweight() * Elemente_anzahl[i][j] * Verbindung_konz[i] / Gesamtgewicht
            else:
                Elemente.append(Symbol)
                Ele_konz.append(Elemente_fkt[i][j].Get_Atomicweight() * Elemente_anzahl[i][j] * Verbindung_konz[i] / Gesamtgewicht)
    Z = 0
    Ele_konz=np.array(Ele_konz)
    Ele_konz=[kon/Ele_konz.sum() for kon in Ele_konz]
    sortlist = []
    for index, e in enumerate(Elemente):
        Z += Element(Element=e).Get_Atomicnumber() * Ele_konz[index]
        sortlist.append(Element(Element=e).Get_Atomicnumber())

    sortierte_liste1, sortierte_liste2, sortierte_liste3 = zip(*sorted(zip(Elemente,Ele_konz, sortlist), key=lambda x: x[2]))
    Elemente = list(sortierte_liste1)
    Ele_konz = list(sortierte_liste2)

    return Elemente, Ele_konz, Z


def Verbindungen_Gewichtsprozent_vonMassenprozent(Verbindungen):
    Verbindung = Verbindungen.split("+")
    #print("Verbindungen:", Verbindung)
    pattern = r'[a-zA-Z]+|\d+\.\d+e[+-]?\d+|\d+e[+-]?\d+|\d+\.\d+|\d+'
    Verbindung_konz = []  # Hier werden die Werte gespeichert, die durch pop entfernt wurden
    bereinigte_verbindungen = []  # Hier werden die Verbindungen ohne die erste Zahl gespeichert

    for i in range(len(Verbindung)):
        result = [float(item) if re.match(r'^\d+\.?\d*(e[+-]?\d+)?$', item) else item for item in re.findall(pattern, Verbindung[i])]
        # Den ersten Wert entfernen und speichern
        konz_wert = result.pop(0)
        Verbindung_konz.append(konz_wert)

        # Erstelle die bereinigte Verbindung ohne die entfernte Zahl
        bereinigte_verbindung = "".join(str(int(item)) if isinstance(item, float) and item.is_integer() else str(item) for item in result)
        bereinigte_verbindungen.append(bereinigte_verbindung)

    Elemente_array = []
    Elemente_konz_array = []
    Verbindung_konz = [x / sum(Verbindung_konz) for x in Verbindung_konz]
    for index, Verb in enumerate(bereinigte_verbindungen):
        x,y = Verbindung_einlesen(Verb)
        #print(x,y,Verbindung_konz[index])
       # print(Verbindung_einlesen(Verb))
        Elemente_array.append(x)
        Elemente_konz_array.append(y * Verbindung_konz[index])
    #print(Elemente_array,Elemente_konz_array)

    Elemente_ret = []
    Konz_ret = []
    for i in range(len(Elemente_array)):
        for j in range(len(Elemente_array[i])):
            Symbol = Elemente_array[i][j]
            if Symbol in Elemente_ret:
                Konz_ret[Elemente_ret.index(Symbol)] += Elemente_konz_array[i][j]
            else:
                Elemente_ret.append(Symbol)
                Konz_ret.append(Elemente_konz_array[i][j])
    Z = 0
    sortlist = []
    for index, e in enumerate(Elemente_ret):
        Z += Element(Element=e).Get_Atomicnumber() * Konz_ret[index]
        sortlist.append(Element(Element=e).Get_Atomicnumber())

    sortierte_liste1, sortierte_liste2, sortierte_liste3 = zip(*sorted(zip(Elemente_ret, Konz_ret, sortlist), key=lambda x: x[2]))
    Elemente_ret = list(sortierte_liste1)
    Konz_ret = list(sortierte_liste2)
    return Elemente_ret, Konz_ret, Z

def Gewichtsprozent_Atomprozent(Elemente, Gewichte):
    Gewichte = np.array(Gewichte)
    Gewichte = np.array([gewicht/Gewichte.sum() for gewicht in Gewichte])
    #print(Gewichte)
    Molmasse=[]
    for index, ele in enumerate(Elemente):
        x_ele = Element(Element=ele)
        Molmasse.append(x_ele.Get_Atomicweight())
    stoffmengenanteil = Gewichte/np.array(Molmasse)
    ret = np.array([i/stoffmengenanteil.sum() for i in stoffmengenanteil])
    return ret, ret/min(ret)

def Filter(Material, Dicke, Energie, Dichte = None, Fenstereinfallwinkel=0):  #Dichte [g/cm**3], Distanz [cm], Material wird zu Massencschwächungskoeffizienten [cm**2/cm]78% Stickstoff, 20,94% Sauerstoff, 0,93% Argon
    if Material.strip().lower() in ["luft", "air"]:
        Dichte = 0.001225
        Elemente = ["N", "O", "Ar"]
        Konzentrationen = np.array([78, 20.94, 0.93])
        Konzentrationen = np.array([con / Konzentrationen.sum() for con in Konzentrationen])
    else:
        #Elemente, Konzentrationen = Verbindung_einlesen(Material)
        Elemente, Konzentrationen,z = Verbindungen_Gewichtsprozent_vonMassenprozent(Material)
    Massenschwächungskoeffizient = 0
    x_Dichte = 0
    for index, i in enumerate(Elemente):
        x_Ele = Element(Element=i)
        Massenschwächungskoeffizient += x_Ele.Massenschwächungskoeffizient(Energie)[1][0] * Konzentrationen[index]
        if Dichte == None:
            x_Dichte += x_Ele.Get_Density() * Konzentrationen[index]
    if x_Dichte != 0:
        Dichte = x_Dichte
    Fenstereinfallwinkel = np.cos(np.pi / 180 * Fenstereinfallwinkel)
    return np.exp(-Massenschwächungskoeffizient * Dichte * Dicke / Fenstereinfallwinkel)



def Filter_array(Material, Dicke, Emin, Emax, step, Dateipfad, Dichte = None, Fenstereinfallwinkel=0):
    if Material.strip().lower() in ["luft", "air"]:
        Dichte = 0.001225
        Elemente_luft = ["N", "O", "Ar"]
        Elemente = [Element(Emin=Emin, Emax=Emax, step=step, Dateipfad=Dateipfad, Element=e) for e in Elemente_luft]
        Konzentrationen = np.array([78, 20.94, 0.93])
        Konzentrationen = np.array([con / Konzentrationen.sum() for con in Konzentrationen])
        #print(Elemente,Konzentrationen)
    else:
        Elemente_str, Konzentrationen = Verbindung_einlesen(Material)
        Elemente = [Element(Emin=Emin, Emax=Emax, step=step, Dateipfad=Dateipfad, Element=e) for e in Elemente_str]
    if Dichte == None:
        x_Dichte = 0
        for index, e in enumerate(Elemente):
            x_Dichte += e.Get_Density() * Konzentrationen[index]
        Dichte = x_Dichte

    Massenschwächungskoeffizient = 0
    for index, e in enumerate(Elemente):
        Massenschwächungskoeffizient += e.Massenschwächungskoeffizient_array()[1] * Konzentrationen[index]
    Fenstereinfallwinkel = np.cos(np.pi / 180 * Fenstereinfallwinkel)
    return Elemente[0].Massenschwächungskoeffizient_array()[0], np.exp(-Massenschwächungskoeffizient * Dichte * Dicke / Fenstereinfallwinkel)

def Z_anpassen(konz_low, z_low, konz_high, z_high, z_gewünscht):
    konz_sum_low = sum(konz_low)
    konz_sum_high = sum(konz_high)
    if konz_sum_low == 0:
        z_mittel_low = sum(np.array(z_low)) / len(z_low)
        z_mittel_high = sum(np.array(konz_high) * np.array(z_high)) / konz_sum_high
        x = (z_gewünscht - z_mittel_high) / (z_mittel_low - z_mittel_high)
        return x, 1-x


    z_mittel_low = sum(np.array(konz_low) * np.array(z_low)) / konz_sum_low
    z_mittel_high = sum(np.array(konz_high) * np.array(z_high)) / konz_sum_high
    konz_gesamt = konz_sum_low + konz_sum_high
    konz_sum_low /= konz_gesamt
    konz_sum_high /= konz_gesamt
    konz_neu_low = ((z_gewünscht - z_mittel_high) / (z_mittel_low - z_mittel_high))
    konz_neu_high = 1 - konz_neu_low
    #konz_gesamt_neu = konz_neu_high + konz_neu_low
    #konz_neu_low /= konz_gesamt_neu
    #konz_neu_high /= konz_gesamt_neu

    if z_gewünscht<z_mittel_low or z_gewünscht>z_mittel_high:
        print(z_mittel_low,z_mittel_high,z_gewünscht, "Wert muss dazwischen liegen")
        ####raise ValueError("Z_gemittel kann nicht erreicht werden!")

    #print("ZPASSEN",konz_neu_low / konz_sum_low, konz_neu_high / konz_sum_high)
    return konz_neu_low / konz_sum_low,  konz_neu_high / konz_sum_high


def str_zu_zahl(string):
    retint = ""
    for i in string:
        if (i == " "):
            retint += str(9)
        elif (i == "K"):
            retint += str(1)
        elif (i == "L"):
            retint += str(2)
        elif (i == "M"):
            retint += str(3)
        elif (i == "N"):
            retint += str(4)
        elif (i == "O"):
            retint += str(5)
        else:
            retint += i
    return(int(retint[0:2]+retint[3:5]))

def zahl_zu_string(zahl):
    def Umwandlung(ziffer):
        if (ziffer == "9"):
            return " "
        elif (ziffer == "1"):
            return "K"
        elif (ziffer == "2"):
            return "L"
        elif (ziffer == "3"):
            return "M"
        elif (ziffer == "4"):
            return "N"
        elif (ziffer == "5"):
            return "O"
        else:
            return "0"
    retstr = ""
    zahl_str = str(zahl)
    retstr += Umwandlung(zahl_str[0])
    if retstr == " ":
        retstr += "K"
    elif retstr == "0":
        return "0"
    else:
        retstr += zahl_str[1]
    retstr += "-"
    retstr += Umwandlung(zahl_str[2])
    retstr += zahl_str[3]
    return retstr

def normiere_daten(data):
    """
    Normiert die Eingabedaten (Liste oder np.array) so, dass ihre Summe 1 ergibt.
    Gibt den gleichen Typ zurück, wie er eingegeben wurde.

    Parameter:
      data (list oder np.array): Die zu normierenden Daten.

    Rückgabe:
      Normierte Daten als list oder np.array (je nach Eingabetyp).
    """
    # Speichern, ob als Liste übergeben wurde
    is_input_list = isinstance(data, list)

    # In NumPy-Array umwandeln (als float, falls nötig)
    arr = np.array(data, dtype=float)

    # Summe berechnen
    s = arr.sum()
    if s == 0:
        raise ValueError("Die Summe der Elemente ist 0, Normierung nicht möglich.")

    normed = arr / s

    # Rückgabe im ursprünglichen Format
    if is_input_list:
        return normed.tolist()
    else:
        return normed


def Grenzen_fix(Konzentrationen, Verhältnis, Grenze=0.05):
    Verhältnis = normiere_daten(Verhältnis)
    gesamtkon = Konzentrationen.sum()
    nor_kon = normiere_daten(Konzentrationen)
    for index, i in enumerate(nor_kon):
        if i > Verhältnis[index] - Grenze and i < Verhältnis[index] + Grenze:
            pass
        elif i < Verhältnis[index] - Grenze:
            nor_kon[index] = Verhältnis[index] - Grenze
        elif i > Verhältnis[index] + Grenze:
            nor_kon[index] = Verhältnis[index] + Grenze
    nor_kon = normiere_daten(nor_kon)
    return np.array(nor_kon) * gesamtkon



def add_format(add, Geometriefaktor):
    add_copy = [element.astype(object) for element in add]
    for index, element in enumerate(add_copy):
        add_copy[index][:, 1] = [zahl*Geometriefaktor for zahl in element[:, 1]]
        add_copy[index][:, 0] = [zahl_zu_string(zahl) for zahl in element[:, 0]]
    return add_copy




def add_arrays_with_concentration(arrays, Konzentration):
    return [
        [] if len(arrays[0][i]) == 0 else [
            sum(Konzentration[idx] * arr[i][j] for idx, arr in enumerate(arrays))
            for j in range(len(arrays[0][i]))
        ]
        for i in range(len(arrays[0]))
    ]

def add_first_four_with_concentration(arrays, Konzentration):
    result = []
    for i in range(len(arrays[0])):  # Durchlaufe die Subarrays
        summed_values = [
            sum(Konzentration[idx] * arr[i][j] for idx, arr in enumerate(arrays)) for j in range(4)
        ]  # Summe der ersten 4 Werte multipliziert mit den Multiplikatoren
        result.append(summed_values)
    return result

