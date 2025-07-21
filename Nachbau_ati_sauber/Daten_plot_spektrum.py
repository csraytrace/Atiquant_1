import cProfile
import pstats
import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.Element import Element


def save_arrays_to_textfile(arrays,Einstellungen, filename):
    with open(filename, 'w') as file:
        for i in range(len(arrays)):
            file.write("#Einstellung: " + Einstellungen[i][0]+"\n")  # Schreibe eine Kopfzeile
            for tupel in arrays[i]:  # Direkt über die Tupel iterieren
                xi, yi, zi = tupel  # Entpacke das Tupel
                file.write(f"{xi}\t{yi}\t{zi}\n")  # Schreibe die Werte in die Datei


def load_arrays_from_textfile(filename):
    arrays = []
    Einstellungen = []
    current_arrays = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            # Überspringe Kommentarzeilen, die mit "#" beginnen
            if line.startswith("#"):
                if line.startswith("#Einstellung:"):
                    # Falls vorherige Daten gesammelt wurden, hinzufügen
                    if current_arrays:
                        arrays.append(current_arrays)
                        current_arrays = []
                    Einstellungen.append([line.replace("#Einstellung: ", "").strip()])
                continue  # Alle anderen Kommentare ignorieren

            # Verarbeite Datenzeilen
            parts = line.split("\t")
            if len(parts) == 3:  # Wenn Zeile valide Daten enthält
                xi = float(parts[0])
                yi = float(parts[1])
                zi = parts[2]
                current_arrays.append((xi, yi, zi))

        # Letzte Gruppe hinzufügen
        if current_arrays:
            arrays.append(current_arrays)
    return arrays, Einstellungen




#rrays = [[(1.2755978351345261e-05, 22.102955679764456, 'Ag'), (1.7180731880452694e-05, 1.487, 'Al')],[(1.2755978351345261e-05, 22.102955679764456, 'Ag'), (1.7180731880452694e-05, 1.487, 'Al')]]
#Einstellung = [["t=0,P=9"],["t=0,P=9"]]

arrays = [[(22.102955679764456, 4.182865970957061e-05, 'Ag'), (1.487, 2.0093160015610797e-05, 'Al'), (23.10792994876348, 4.4003895816415674e-05, 'Cd'), (8.041215748748293, 3.092335181235477e-05, 'Cu'), (1.739334980440601, 2.4899278665853156e-05, 'Si'), (4.507980015896446, 3.3710882337434494e-05, 'Ti'), (4.949304535637149, 3.231046967944464e-05, 'V'), (8.631189867640346, 3.1999721083465646e-05, 'Zn'), (15.746151182987512, 3.7062480934936805e-05, 'Zr'), (2.9833908176471926, 4.243065004260396e-05, 'Ag_L'), (10.82794806552806, 3.200211895713583e-05, 'Bi_L'), (3.1323908092068327, 3.312357292093657e-05, 'Cd_L'), (10.540562082673976, 3.039701316722293e-05, 'Pb_L'), (3.443187787468415, 4.299107691272522e-05, 'Sn_L'), (8.139111104249773, 3.2240240808273864e-05, 'Ta_L')], [(22.102955679764456, 2.7974364160346087e-05, 'Ag'), (1.487, 2.008292669486116e-05, 'Al'), (23.10792994876348, 2.8024104846810228e-05, 'Cd'), (8.041215748748293, 2.6601023531216985e-05, 'Cu'), (1.739334980440601, 2.4850581234781094e-05, 'Si'), (4.507980015896446, 3.088955655380787e-05, 'Ti'), (4.949304535637149, 2.9357045523802037e-05, 'V'), (8.631189867640346, 2.7289362849794637e-05, 'Zn'), (15.746151182987512, 2.8447241364671868e-05, 'Zr'), (2.9833908176471926, 4.025639143871985e-05, 'Ag_L'), (10.82794806552806, 2.6179041440619014e-05, 'Bi_L'), (3.1323908092068327, 3.1290301336988714e-05, 'Cd_L'), (10.540562082673976, 2.5001605161335614e-05, 'Pb_L'), (3.443187787468415, 4.0366292128699174e-05, 'Sn_L'), (8.139111104249773, 2.7637953211529504e-05, 'Ta_L')]]
Einstellung= [['Messzeit=30, Röhrenstrom=0.01, Emax=3.70e+01'], ['Messzeit=30, Röhrenstrom=0.01, Emax=4.00e+01']]


save_arrays_to_textfile(arrays,Einstellung,filename="output.txt")
#print(load_arrays_from_textfile("output.txt"))
