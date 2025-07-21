import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
import struct
from io import BytesIO
import base64

#import PyMca5.tests
#PyMca5.tests.testAll()
import sys
import PyQt5
from PyMca5.PyMcaGui.pymca import PyMcaMain



file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\12.06.24, nofil,vak\\0.02mA,150s,30V\\SPECTRUM.210'
#file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\CS\\SPECTRUM.202'
integer_text_file_path = 'C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Tracormessungen\\integer_output.txt'
with open(file_path, 'rb') as file:
    content = file.read()

print(content[0:46])
#for i in range(14):
#    print(content[i+12:1024])


print("L",len(content))


werte = []
werte_int_short = []
char_wert = []
x = []
a, e = 46, 2094

for i in range(len(content)//4):
    werte.append(struct.unpack('i', content[i*4:i*4+4])[0])
    x.append(i*0.02-a*0.02)
for i in range(len(content)//2):
    werte_int_short.append(struct.unpack('H', content[i*2:i*2+2])[0])
    #x.append(i*0.02-a*0.02)





for i in range(len(content[:a*4])):
    char_wert.append(struct.unpack('c', content[i+a*4:i+a*4+1])[0])
    if(struct.unpack('c', content[i+a*4:i+a*4+1])[0] == b'T'):
        print("existA")
for i in range(len(content[e*4:])):
    char_wert.append(struct.unpack('c', content[i+e*4:i+e*4+1])[0])
    if(struct.unpack('c', content[i+e*4:i+e*4+1])[0] == b'T'):
        print("existE")

#print(werte)
print(char_wert)
print(werte[0:a])
print(werte[e:])

plt.plot(x[a:e],werte[a:e], color="g", label = "char")
print("short",werte_int_short[-15])
print("short",werte_int_short)
plt.legend()
#plt.show()
def write_to_text_file(data, output_path):
    with open(output_path, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

write_to_text_file(werte[a:e], integer_text_file_path)


#for v,i in enumerate(werte_int_short):
   # if i == 30:
      #  print(v)
print(werte_int_short[4188])
print(werte_int_short[4150:4200])
print(char_wert[4:13])
