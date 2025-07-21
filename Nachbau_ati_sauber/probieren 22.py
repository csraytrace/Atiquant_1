import tkinter as tk
from tkinter import messagebox
from Nachbau_ati_sauber.Element import Element


def A(zahl):
    return str(f"{zahl:.3f}")
# Funktion zur Berechnung der Summe
def berechne_element():
    try:
        wert1 = entry1.get()
        wert2 = entry2.get()
        x = Element(Element = wert1)
        Energie = float(wert2)

        K_übergänge = [" K-L2", " K-L3"]
        L_übergänge = ["L3-M4", "L3-M5"]
        Ka, La = 0, 0


        for i in x.Ubergange():
            if (i[0] in K_übergänge):
                Ka += i[2]
            if (i[0] in L_übergänge):
                La += i[2]

        label_ergebnis.config(text=f"Ergebnis:\nElement: " + x.Get_Elementsymbol()+"\t"+str(int(x.Get_Atomicnumber()))+"\nCosta_Kronig f1,f12,f13,f´13, f23:"+str(x.Costa_Kronig())+
                              "\nFluoreszenzausbeute"+ str([(i[0][6:], float(i[1])) for i in x.Omega()])+"\nÜberganswahrscheinlichkeit"+str([(i[0], i[2]) for i in x.Ubergange() if i[0] in K_übergänge])+"Ka: "+str(f"{Ka:.3f}")
                                   +"\nÜberganswahrscheinlichkeit"+str([(i[0], i[2]) for i in x.Ubergange() if i[0] in L_übergänge])+"La: "+str(f"{La:.3f}")+"\n\nMassenabsorptionskoeffizient Tau:"+ A(x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g())+
                                   " [barns/atom]\n Sij(K,Energie):"+A(x.S_ij(" K", Energie))+"\tSij * Tau:"+A(x.S_ij(" K", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g())
                              +"\n Sij(L3,Energie):"+A(x.S_ij(" L3", Energie))+"\tSij * Tau:"+A(x.S_ij("L3", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g())+"\n Sij(L2,Energie):"
                                   +A(x.S_ij(" L2", Energie))+"\tSij * Tau:"+A(x.S_ij("L2", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g())+
                                   "\n Sij(L1,Energie):"+A(x.S_ij(" L1", Energie))+"\tSij * Tau:"+A(x.S_ij("L1", Energie) * x.Massenabsorptionskoeffizient(Energie)[1][0]/x.Get_cm2g()))
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Elementinfo")
root.geometry("700x600")  # Fenstergröße anpassen

# Label und Eingabefeld für den ersten Wert
label1 = tk.Label(root, text="Element:", font=("Arial", 14))
label1.pack(pady=10)  # Abstand vergrößern
entry1 = tk.Entry(root, font=("Arial", 14), width=10)
entry1.pack(pady=5)
entry1.insert(0, "Cd")  # Standardwert "Cd" einfügen

# Label und Eingabefeld für den zweiten Wert
label2 = tk.Label(root, text="Energie[keV]:", font=("Arial", 14))
label2.pack(pady=10)  # Abstand vergrößern
entry2 = tk.Entry(root, font=("Arial", 14), width=10)
entry2.pack(pady=5)
entry2.insert(0, "10")  # Standardwert "10" einfügen

# Button zur Berechnung
button = tk.Button(root, text="Berechne Tau", font=("Arial", 14), command=berechne_element)
button.pack(pady=20)

# Label zur Anzeige des Ergebnisses
label_ergebnis = tk.Label(root, text="Ergebnis: ", font=("Arial", 14))
label_ergebnis.pack(pady=20)

# Ereignisschleife starten
root.mainloop()
