import matplotlib.pyplot as plt
import struct
import numpy as np
from Nachbau_ati_sauber.peak_calc import *
from datetime import datetime


def Read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content

def Convert_to_int(binary):
    int_werte = []
    x_werte = []
    for i in range(len(binary)//4):
        int_werte.append(struct.unpack('i', binary[i*4:i*4+4])[0])
        #x_werte.append(i*40 /2048)
        x_werte.append(i*0.02)
    #return np.array(int_werte), np.array(x_werte)
    #print(len(int_werte))
    return [int_werte, x_werte]

def Convert_to_char(binary):
    char_werte = ""
    for i in range(len(binary)):
        #char_werte.append(struct.unpack('c', binary[i:i+1])[0].decode("utf-8"))
        buchstabe = struct.unpack('c', binary[i:i+1])[0].decode("utf-8")
        if (buchstabe.isalpha() or buchstabe.isspace() or buchstabe.isdigit()):
            char_werte += struct.unpack('c', binary[i:i+1])[0].decode("utf-8")
    return char_werte

def Convert_to_short(binary):
    shor_werte = []
    for i in range(len(binary)//2):
        shor_werte.append(struct.unpack('H', binary[i*2:i*2+2])[0])
    return shor_werte

def Tracor_daten(file_path, plot, info, intensity = None, save_fig = [False, "_"]):    #save_fig [true/false, dateipfad]
    content = Read_file(file_path)
    if (len(content) == 8424):
        y_spec , x_werte = Convert_to_int(content[184:8376])

    if (len(content) == 4328):
        y_spec , x_werte = Convert_to_int(content[184:4280])

    if (len(content) == 2280):
        y_spec , x_werte = Convert_to_int(content[184:2232])

    if (info):
        print("Messzeit:", Convert_to_short(content[-30:-28])[0],"sec", ",Spannung:", Convert_to_short(content[-48:-46])[0], "kV", ",Strom:", Convert_to_short(content[-46:-44])[0]*10**-2,"mA")
        print("Name:",Convert_to_char(content[22:35]), ",Filter:", Convert_to_char(content[-44:-35]), ",L/V:", Convert_to_char(content[-14:-8]))
        #print(Convert_to_short(content[8376:8378])[0] == Convert_to_short(content[-48:-46])[0])
        #print(Convert_to_short(content[8378:8380])[0]  == Convert_to_short(content[-46:-44])[0])
        #print(Convert_to_char(content[8380:8389]) ==Convert_to_char(content[-44:-35]) )
       # if (Convert_to_char(content[22:26])=="CD"):
          #  print()
          #  print()
    if (plot):
        plt.plot(x_werte,y_spec, color="g", label = "Spektrum")
        plt.title(Convert_to_char(content[22:35]))
        plt.xlabel("E [keV]")
        plt.ylabel("Counts")
        plt.legend()
        plt.show()

    if (save_fig[0]):
        def format_number(num, leerzeichen=8):
            # Konvertiere die Zahl in einen String und fülle mit Leerzeichen, sodass die Gesamtlänge 8 ist
            return str(num).rjust(leerzeichen)

        with open(save_fig[1]+Convert_to_char(content[22:35])+".spe", "w") as file:
            file.write("$SPEC_ID:\n")
            file.write(Convert_to_char(content[22:35]))
            file.write("\n")
            file.write("$DATE_MEA:\n")
            file.write(datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
            file.write("\n")
            file.write("$MEAS_TIM:\n")
            file.write(format_number(Convert_to_short(content[-30:-28])[0]))
            file.write("\n")
            file.write("$Info:\n")
            file.write("Messzeit:" +str(Convert_to_short(content[-30:-28])[0])+"sec, Spannung:"+str(Convert_to_short(content[-48:-46])[0])+"kV, Strom:"+ str(Convert_to_short(content[-46:-44])[0]*10**-2)+"mA\n")
            file.write("Name:"+str(Convert_to_char(content[22:35]))+ ", Filter:"+str(Convert_to_char(content[-44:-35]))+ ", L/V:"+ str(Convert_to_char(content[-14:-8]))+"\n")
            file.write("$DATA:\n")
            file.write(format_number(0,10))
            file.write(format_number(len(x_werte)-1,10))
            file.write("\n")
            for i in range(len(x_werte)):
                file.write(format_number(y_spec[i]))
                if i % 10 == 0:
                    file.write("\n")

    if (intensity[0] == True):      # ja/nein  minimale Höhe Ort vom Peak
        Intensitätsklasse = Intensity([y_spec , x_werte],  min_y = intensity[1], peak = intensity[2], titel = Convert_to_char(content[22:35]))
        netarea = Intensitätsklasse.Plot()
        plt.show()
        return y_spec, netarea, (Convert_to_char(content[22:35]))
    return [y_spec, x_werte], (Convert_to_char(content[22:35]))

#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.02mA,150s,30V\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\L_linien\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\fremdeMessungen\\GG\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\fremdeMessungen\\NECKER\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\fremdeMessungen\\KESSELST\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\Z_BESTIM\\SPECTRUM.'
file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\STD\\SPECTRUM.'
##file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\wobi\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\KLAUD\\SPECTRUM.'
save = file_path[:-9]

int = []
dateianfang = 110
for i in range(8):
    print("Datei", dateianfang+i)
    y_spec,title=Tracor_daten(file_path+str(dateianfang+i), 0, 1, (0,15000,None), [True,save])
    #print(process_peaks(y_spec[0],y_spec[1],19.2,20,show_plot=True))

    ##print(process_intervals(y_spec[0],y_spec[1],[18.6,19.86],[19.86,20.59],titel1=title))

    #int.append((Tracor_daten(file_path+str(100+i), 0, 0, (1,100,None), [True,save])[1:]))
    #print(y)

#20.1 19.2
#Tracor_daten(file_path+str(103), 0, 1, (0,104,None), [True,save])

#y_spec=Tracor_daten(file_path+str(103), 0, 1, (0,104,20.1), [True,save])
#print(y_spec[0],y_spec[1])

#process_peaks(y_spec[0],y_spec[1],19.2,20)
#y_spec=Tracor_daten(file_path+str(144), 0, 1, (0,104,20.1), [False,save])
#print(process_intervals(y_spec[0],y_spec[1],[19.86,20.59],[14,19.86]))
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\Z_low\\SPECTRUM.'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Messung2025\\Z_BESTIM\\SPECTRUM.'
#y_spec=Tracor_daten(file_path+str(209), 0, 1, (0,104,20.1), [False,save])

"""
title_list=[]
x,y,z = [],[],[]
for i in range(1):
    y_spec,title=Tracor_daten(file_path+str(144+i), 0, 1, (0,100,None), [False,save])
    title_list.append(title)
    #x1,y1,z1 = (process_peaks(y_spec[0],y_spec[1],20,19.2,show_plot=False))
    x1,y1,z1 = process_intervals(y_spec[0],y_spec[1],[18.6,19.86],[19.86,20.59],show_plot=True,titel1=title)
    x.append(x1)
    y.append(y1)
    z.append(z1)

print(x,y,z)
print(title_list)

"""
#Tracor_daten(file_path+str(111), 0, 1, (1,104,19.25), [True,save])

#Tracor_daten(file_path+str(121), 0, 1, (1,2,34.7), [True,save])


#Tracor_daten(file_path+str(150), 0, 1, (1,90,None), [True,save])
#Tracor_daten(file_path+str(151), 0, 1, (1,90,None), [True,save])


"""

x_wert = np.arange(0,2048*0.02,0.02)
y=[]
y.append(Tracor_daten(file_path+str(112), 0, 0, (0,90,None), [False,save])[0])
y.append(Tracor_daten(file_path+str(113), 0, 0, (0,90,None), [False,save])[0])
print(y[0])
plt.plot(x_wert,y[0][0], color="g", label = "Spektrum 112")
plt.plot(x_wert,y[1][0], color="b", label = "Spektrum 113")
plt.legend()
plt.show()
y=[]
"""
"""
y.append(Tracor_daten(file_path+str(111), 0, 0, (0,90,None), [False,save]))
y.append(Tracor_daten(file_path+str(123), 0, 0, (0,90,None), [False,save]))
y.append(Tracor_daten(file_path+str(151), 0, 0, (0,90,None), [False,save]))


x_wert = np.arange(0,2048*0.02,0.02)
print(x_wert)
plt.plot(x_wert,y[0], color="g", label = "Spektrum")
plt.plot(x_wert,y[1], color="b", label = "Spektrum")
plt.plot(x_wert,y[2], color="r", label = "Spektrum")
#plt.show()


y=[]
y.append(Tracor_daten(file_path+str(112), 0, 0, (0,90,None), [False,save]))
y.append(Tracor_daten(file_path+str(120), 0, 0, (0,90,None), [False,save]))
y.append(Tracor_daten(file_path+str(150), 0, 0, (0,90,None), [False,save]))


x_wert = np.arange(0,2048*0.02,0.02)

#plt.plot(x_wert,y[0], color="g", label = "Spektrum")
plt.plot(x_wert,y[1], color="b", label = "Spektrum")
plt.plot(x_wert,y[2], color="r", label = "Spektrum")
#plt.show()

"""

#Tracor_daten(file_path+str(140), 0, 1, (1,1000,4.8), [True,save])
#Tracor_daten(file_path+str(144), 0, 1, (1,1000,4.8), [True,save])
#Tracor_daten(file_path+str(132), 0, 1, (1,1000,8), [True,save])

#Tracor_daten(file_path+str(117), 0, 1, (1,2,34.5), [True,save])
#Tracor_daten(file_path+str(117), 0, 1, (1,20,2.2), [True,save])
#Tracor_daten(file_path+str(113), 0, 1, (1,90,4.8), [True,save])
#Tracor_daten(file_path+str(101), 0, 1, (1,20,None), [True,save])
#Tracor_daten(file_path+str(112), 0, 1, (1,20,None), [True,save])
#Tracor_daten(file_path+str(117), 0, 1, (1,20,None), [True,save])

#print(int)
##Tracor_daten(file_path+str(100+2), 0, 1, (1,900,3.13))
#Tracor_daten(file_path+str(205), 0, 1, (0,100,23.1), [True, "C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracor_spek\\test.spe"])

#Tracor_daten(file_path+str(205), 0, 1, (1,100,3))

#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\Standardmessungen\\SPECTRUM.249'
#Tracor_daten(file_path, 0, 1, (1,2000,120))
#tupel ( true, min_y = 100, peak = None

#content = Read_file(file_path+str(200+19))
#print(content)
#print(len(Read_file(file_path+str(200+49))))


"""
Tracor_daten(file_path+str(200+1), plot = 0, info = 1, intensity=(1,1700,None))
Tracor_daten(file_path+str(200+2), plot = 0, info = 1, intensity=(1,400,None))
Tracor_daten(file_path+str(200+3), plot = 0, info = 1, intensity=(1,400,1100))
Tracor_daten(file_path+str(200+4), plot = 0, info = 1, intensity=(1,400,None))
Tracor_daten(file_path+str(200+5), plot = 0, info = 1, intensity=(1,80,1150))

Tracor_daten(file_path+str(200+6), plot = 0, info = 1, intensity=(1,400,None))
Tracor_daten(file_path+str(200+7), plot = 0, info = 1, intensity=(1,400,None))
Tracor_daten(file_path+str(200+8), plot = 0, info = 1, intensity=(1,460,None))
Tracor_daten(file_path+str(200+9), plot = 0, info = 1, intensity=(1,400,None))
Tracor_daten(file_path+str(200+0), plot = 0, info = 1, intensity=(1,3200,None))
"""


