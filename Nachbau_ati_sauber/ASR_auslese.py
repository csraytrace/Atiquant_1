import glob
from Nachbau_ati_sauber.Calc_I import Calc_I

def Einlesen_ausgabe(folder_path):
    daten = []
    with open(folder_path, 'r') as file:
        for row in file:
            daten.append(row.rstrip('\n ').rstrip(','))
    return (int(list(filter(None, daten[-1].split(" ")))[0]), int(list(filter(None, daten[-1].split(" ")))[3].rstrip(".")))

def All_asr_files(path):
    file_list = glob.glob(path)
    liste = []
    for data in file_list:
        liste.append(Einlesen_ausgabe(data))
    return liste
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.02mA,150s,30V\\AL_1.ASR'
# Pfad zu den Dateien mit der Endung .asr
path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.02mA,150s,30V\\*.asr'
#print(All_asr_files(path))


