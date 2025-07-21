import numpy as np
from Nachbau_ati_sauber.packages.Massenschwächungskoeffizient import Massenschwächungskoeffizient
from Nachbau_ati_sauber.packages.Auslesen import Datenauslesen
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Detektor import Detektor
from Nachbau_ati_sauber.Calc_I import Calc_I
from Nachbau_ati_sauber.ASR_auslese import All_asr_files
from Nachbau_ati_sauber.packages.Funktionen import call_function_with_config
from Nachbau_ati_sauber.packages.Funktionen import call_class_with_config
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
from Nachbau_ati_sauber.Geoplot_klasse import InteractivePlot
from itertools import product
from Nachbau_ati_sauber.Daten_plot_spektrum import save_arrays_to_textfile


#def counter(Übergänge, array):
#    sum = 0
 #   for über in array:
 #       if über[0] in Übergänge:
#            sum += über[1]
#    return sum
#Kbeta = [" K-M1", " K-M2", " K-M3", " K-M4", " K-M5"]
#Kalpha = [" K-L1", " K-L2", " K-L3"]
#Lalpha = ["L3-M4", "L3-M5"]


def parameter_änderung(para_var, grenzen, stepanzahl, para = ""):   #Elementanzahl erhält ab 11

    Einstellung = []
    if (isinstance(para_var , (list))):
        para_var = para_var[0]
    Detektor = False

    if para_var.strip() in ["Fensterdicke_det", "phi_det", "Kontaktmaterialdicke", "Bedeckungsfaktor", "Totschicht", "activeLayer"]:
        Detektor = True


    distanz = (grenzen[1] - grenzen[0])
    variationsbereich = [grenzen[0] + x * distanz / (stepanzahl - 1) for x in range(stepanzahl)]
    x_werte = []    #einmal alle Übergänge
    y_werte = []    #stepanzahl * alle Übergänge
    z_zeichen = []

    for x in variationsbereich:
        Einstellung.append(para_var + "=" + f"{x:.4e}")

    if para_var.strip() == "Emax":
        Emax = min(grenzen)
    else:
        if (isinstance(para, str) and len(para) > 1):
            Emax = call_class_with_config(Calc_I,Einstellung[0] + ", " + para).Emax
        else:
            Emax = call_class_with_config(Calc_I,Einstellung[0]).Emax

    for x_z in range(11,95):
        x_ele=Element(Element=x_z)
        if (x_ele.Kanten()[0][1] >= Emax):
            break
        x_werte.append(x_ele.K_gemittel_ubergang())
        z_zeichen.append(x_ele.Get_Elementsymbol())
        Elementanzahl=x_z


    y_2 = []
    x_2 = []
    for index, parameter in enumerate(Einstellung):
        werte = parameter
        if (isinstance(para, str) and len(para) > 1):
            werte += ", " + para

        if para_var == "Einfallswinkelalpha":
            werte += ", Einfallswinkelbeta" + "=" + f"{90-variationsbereich[index]:.4e}"
            print(werte)

        if para_var == "Einfallswinkelbeta":
            werte += ", Einfallswinkelalpha" + "=" + f"{90-variationsbereich[index]:.4e}"
            print(werte)

        y_durchgang = []

        Ki = call_class_with_config(Calc_I,werte)
        if not Detektor:
            #y_2.append(Ki.Röhre.Countrate_gesamt[1])
            y_2.append(Ki.Röhre.Gesamtspektrum_plot[1])
            if para_var.strip() == "Emax":
                #x_2.append(Ki.Röhre.Countrate_gesamt[0])
                x_2.append(Ki.Röhre.Gesamtspektrum_plot[0])
        if Detektor:
            y_2.append(Ki.Detektor.Detektorspektrum()[1])

        for i in range(11,Elementanzahl+1):
            print(i)

            Ki = call_class_with_config(Calc_I,werte + ", P1=["+str(i)+"]")
            y_durchgang.append(1/Ki.Intensität_alle_jit_fürMinimierung([1])[0][0])
        y_werte.append(y_durchgang)

    if para_var.strip() != "Emax":
        x_2 = Ki.Röhre.Countrate_gesamt[0]
    x_werte = np.array(x_werte)
    y_werte = np.array(y_werte)
    y_werte /= y_werte[len(y_werte) // 2]
    #y_werte /= y_werte[2]
    return x_werte, y_werte, z_zeichen, x_2, y_2


#x,y, z, x2, y2 =parameter_änderung(" Emax", [15,17],2)
##x,y, z, x2, y2 =parameter_änderung(" Fensterdicke_det", [7,8],2,para="Emax=12")
#x,y, z, x2, y2 =parameter_änderung(" Fensterdicke_det", [7,8],3,para="Emax=40")

def plots(Parameter=["charzucont"], Grenzen = [[1.2,0.8]], Zusatz=r" ", log_y2 = [False], Speichererweiterung = False):
    savefig=False


    x_a, y_a, z_a, x2_a, y2_a = [],[],[],[],[]
    for i in range(len(Grenzen)):
        if Parameter[i] == "Emax":
            para="step=0.005"
        else:
            para = "Emax=40, step=0.005"
        print("durchlauf",i)

        x,y, z, x2, y2 =parameter_änderung(Parameter[i], Grenzen[i], 3, para=para)
        x_a.append(x)
        y_a.append(y)
        z_a.append(z)
        x2_a.append(x2)
        y2_a.append(y2)


    for i in range(len(Grenzen)):
        linewidth=2

        if Parameter[i] == "Emax":
            linewidth=1

        if Parameter[i] == "charzucont":
            ymin2=10**10
            ymax2=8*10**11

        if Parameter[i] == "charzucont_L":
            ymin2=10**9
            ymax2=1.8*10**12

        elif log_y2[i]:
            ymin2=4*10**8
            ymax2=8*10**10

        else:
            ymin2=np.min(y2_a[i]) * 0.99
            ymax2=np.max(y2_a[i]) * 1.01

        ymin=np.min(y_a[i])*0.99
        ymax=np.max(y_a[i]) *1.01

        Grenzen_i = Grenzen[i]
        Grenzen_i.insert(1,(Grenzen_i[0] + Grenzen_i[1]) / 2)

        label = [str(Grenzen_i[0])+Zusatz[i], str(Grenzen_i[1])+Zusatz[i], str(Grenzen_i[2])+Zusatz[i]]

        Titel = "Änderung"+" "+Parameter[i]
        if Parameter[i] == "Einfallswinkelalpha":
            Titel = r"Einfallswinkel $\alpha$ und $\beta$"
            label = [str(Grenzen_i[0])+Zusatz[i] + str(90 - Grenzen_i[0]), str(Grenzen_i[1])+Zusatz[i]+ str(90 - Grenzen_i[1]), str(Grenzen_i[2])+Zusatz[i]+str(90 - Grenzen_i[2])]
        ylabel="%-Änderung des Geometriefaktors (gestrichelt ----)"
        if log_y2[i]:
            ylabel2="Röhrenspektrum (Linie ────)"
        else:
            ylabel2="Detektoreffizienz (Linie ────)"


        fig, ax = plt.subplots()
        ax2 = ax.twinx()  # Eine einzige y2-Achse für alle Linien

        ax2.set_ylim(ymin2, ymax2)
        ax2.yaxis.set_visible(False)
        # Plotte die Linien (Hauptachse y1)
        if Parameter[i] == "Emax":
            Plot_einfach([x_a[i], y_a[i][0], x2_a[i][0], y2_a[i][0]]).plot_line(ax=ax, ax2=ax2, color="b", label=label[0], label2=None, color2="b", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
            Plot_einfach([x_a[i], y_a[i][1], x2_a[i][1], y2_a[i][1]]).plot_line(ax=ax, ax2=ax2, color="r", label=label[1], label2=None, color2="r", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
            Plot_einfach([x_a[i], y_a[i][2], x2_a[i][2], y2_a[i][2]]).plot_line(ax=ax, ax2=ax2, color="g", label=label[2], label2=None, color2="g", ylabel2=ylabel2, log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")

            Plot_einfach([x_a[i], y_a[i][1],z_a[i]]).plot_scatter(ax=ax, ax2=ax2, color="r", label=None, label2=None, color2="r", point_size=20, title=Titel, ylabel=ylabel,ymin=ymin,ymax=ymax)
        else:
            Plot_einfach([x_a[i], y_a[i][0], x2_a[i], y2_a[i][0]]).plot_line(ax=ax, ax2=ax2, color="b", label=label[0], label2=None, color2="b", ylabel2="", log_y2=log_y2[i], ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
            Plot_einfach([x_a[i], y_a[i][1], x2_a[i], y2_a[i][1]]).plot_line(ax=ax, ax2=ax2, color="r", label=label[1], label2=None, color2="r", ylabel2="", log_y2=log_y2[i], ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
            Plot_einfach([x_a[i], y_a[i][2], x2_a[i], y2_a[i][2]]).plot_line(ax=ax, ax2=ax2, color="g", label=label[2], label2=None, color2="g", ylabel2=ylabel2, log_y2=log_y2[i], ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")

            Plot_einfach([x_a[i], y_a[i][1],z_a[i]]).plot_scatter(ax=ax, ax2=ax2, color="r", label=None, label2=None, color2="r", point_size=20, title=Titel, ylabel=ylabel,ymin=ymin,ymax=ymax)

        ax.legend(loc="upper right")
        if savefig:
            fig = plt.gcf()
            fig.set_size_inches(16, 9)
            Speicherplus = ""
            if Speichererweiterung:
                Speicherplus += "_"+str(Grenzen_i[0])+"-"+str(Grenzen_i[-1])

            plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Präsentation_2\\Parametervariation_2\\"+Parameter[i]+Speicherplus+".png", dpi=600, bbox_inches="tight")
        plt.show()




Parameter = ["charzucont","Einfallswinkelalpha","Einfallswinkelalpha","Emax","Emax","sigma","sigma","activeLayer","activeLayer","Totschicht", "Kontaktmaterialdicke"]
Grenzen = [[1.2,0.8],[19,21],[15,25],[39,41],[30,32],[1.0214,1.0414],[0.8,1],[2.9,3.1],[2,4],[0.02,0.08], [40,60]]
Zusatz = [r"", " und ", " und "," kV"," kV",r"",r"",r" mm",r" mm", r" $\mu$m"," nm"]
log_y2 = [True,True,True,True,True,True,True,False,False,False,False]

Parameter = ["activeLayer","activeLayer","Totschicht", "Kontaktmaterialdicke"]
Grenzen = [[2.9,3.1],[2,4],[0.02,0.08], [40,60]]
Zusatz = [r" mm",r" mm", r" $\mu$m"," nm"]
log_y2 = [False,False,False,False]

Parameter = ["charzucont_L"]
Grenzen = [[1.9,0.1]]
Zusatz = [r""]
log_y2 = [True]
#plots()
#plots(Parameter=["charzucont","Einfallswinkelalpha"], Grenzen = [[1.2,0.8],[19,21]] , Zusatz=[r"", " und "], log_y2 = [True,True],Speichererweiterung=True)
plots(Parameter=Parameter, Grenzen=Grenzen, Zusatz=Zusatz, log_y2=log_y2, Speichererweiterung=True)


savefig=True

Grenzen = [1.2,0.8]
Parameter="charzucont"
Zusatz=r" "

#ymin2=4*10**8   #sigma
#ymax2=8*10**10

#ymin2=10**10    #carzuconst
#ymax2=8*10**11

log_y2 = False

linewidth=2

x,y, z, x2, y2 =parameter_änderung(Parameter, Grenzen,3,para="Emax=40, step=2")

ymin2=np.min(y2) * 0.99
ymax2=np.max(y2) * 1.01

Titel = "Änderung"+" "+Parameter
#Titel = r"Einfallswinkel $\alpha$ und $\beta$"
ylabel="%-Änderung des Geometriefaktors (gestrichelt ----)"
ylabel2="Detektoreffizienz (Linie ────)"
#ylabel2="Röhrenspektrum"

Grenzen.insert(1,(Grenzen[0] + Grenzen[1]) / 2)
# Erstelle eine gemeinsame Hauptachse für alle Plots


#Plot_einfach([ x2, y2[0]]).plot_line(color="b", label=str(Grenzen[0])+Zusatz, log_y=True)
#Plot_einfach([ x2, y2[1]]).plot_line(color="r", label=str(Grenzen[1])+Zusatz, log_y=True)
#Plot_einfach([ x2, y2[2]]).plot_line(color="g", label=str(Grenzen[2])+Zusatz, log_y=True)

#plt.show()



fig, ax = plt.subplots()
ax2 = ax.twinx()  # Eine einzige y2-Achse für alle Linien

ymin=np.min(y)*0.99
#ymin2=np.min(y2) * 0.9
ymax=np.max(y) *1.01
#ymax2=np.max(y2) * 1.1

#ax2.set_ylim(ymin2, ymax2)
#ax2.set_ylim(10**7, 3*10**10)


#ymin2=5*10**2
#ymax2=7.5*10**11
#ax2.set_ylim(ymin2*0.9, ymax2*1.1)
ax2.set_ylim(ymin2, ymax2)
ax2.yaxis.set_visible(False)
#ymin2*=0.9
#ymax2*=1.1
# Plotte die Linien (Hauptachse y1)
Plot_einfach([x, y[0], x2, y2[0]]).plot_line(ax=ax, ax2=ax2, color="b", label=str(Grenzen[0])+Zusatz, label2=None, color2="b", ylabel2="", log_y2=log_y2, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
Plot_einfach([x, y[1], x2, y2[1]]).plot_line(ax=ax, ax2=ax2, color="r", label=str(Grenzen[1])+Zusatz, label2=None, color2="r", ylabel2="", log_y2=log_y2, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")
Plot_einfach([x, y[2], x2, y2[2]]).plot_line(ax=ax, ax2=ax2, color="g", label=str(Grenzen[2])+Zusatz, label2=None, color2="g", ylabel2=ylabel2, log_y2=log_y2, ymin2=ymin2, ymax2=ymax2, linewidth=1, linestyle="--")

#Plot_einfach([x, y[3], x2, y2[3]]).plot_line(ax=ax, ax2=ax2, color="y", label="Det4", label2=None, color2="y", ylabel2="dadat")
#Plot_einfach([x, y[4], x2, y2[4]]).plot_line(ax=ax, ax2=ax2, color="purple", label="Det5", label2=None, color2="purple", ylabel2="dadat")

#Plot_einfach([x, y[0], x2[0], y2[0]]).plot_line(ax=ax, ax2=ax2, color="b", label=str(Grenzen[0])+Zusatz, label2=None, color2="b", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1)
#Plot_einfach([x, y[1], x2[1], y2[1]]).plot_line(ax=ax, ax2=ax2, color="r", label=str(Grenzen[1])+Zusatz, label2=None, color2="r", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1)
#Plot_einfach([x, y[2], x2[2], y2[2]]).plot_line(ax=ax, ax2=ax2, color="g", label=str(Grenzen[2])+Zusatz, label2=None, color2="g", ylabel2=ylabel2, log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth=1)



#Plot_einfach([x, y[2], x2, y2[2]]).plot_line(ax=ax, ax2=ax2, color="g", label=str(Grenzen[2])+Zusatz, label2=None, color2="g", ylabel2=ylabel2, log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth2=linewidth)
#Plot_einfach([x, y[1], x2, y2[1]]).plot_line(ax=ax, ax2=ax2, color="r", label=str(Grenzen[1])+Zusatz, label2=None, color2="r", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth2=linewidth)
#Plot_einfach([x, y[0], x2, y2[0]]).plot_line(ax=ax, ax2=ax2, color="b", label=str(Grenzen[0])+Zusatz, label2=None, color2="b", ylabel2="", log_y2=True, ymin2=ymin2, ymax2=ymax2, linewidth2=linewidth)

Plot_einfach([x, y[1],z]).plot_scatter(ax=ax, ax2=ax2, color="r", label=None, label2=None, color2="r", point_size=20, title=Titel, ylabel=ylabel,ymin=ymin,ymax=ymax)

ax.legend(loc="upper right")

if savefig:

    fig = plt.gcf()
    fig.set_size_inches(16, 9)

    #plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Präsentation_2\\Parametervariation_2\\"+Parameter+".png", dpi=600, bbox_inches="tight")
#plt.show()



Plot_einfach([ x2, y2[0]]).plot_line(color="b", label=str(Grenzen[0])+Zusatz)
Plot_einfach([ x2, y2[1]]).plot_line(color="r", label=str(Grenzen[1])+Zusatz)
Plot_einfach([ x2, y2[2]]).plot_line(color="g", label=str(Grenzen[2])+Zusatz)



#plt.show()

fig, ax = plt.subplots()

# Erstelle zwei getrennte y2-Achsen
ax2_1 = ax.twinx()

##ax2_2 = ax.twinx()



ymin=np.min(y) * 0.9
ymin2=np.min(y2) * 0.9
ymax=np.max(y) * 1.1
ymax2=np.max(y2) * 1.1

# Beide Achsen haben dieselbe Skalierung
ax2_1.set_ylim(ymin2, ymax2)
##ax2_2.set_ylim(ymin2, ymax2)

Plot_einfach([x, y[0], x2, y2[0]]).plot_line(ax=ax, ax2=ax2_1, color="b", label="Det1", label2="l1",color2="b")
Plot_einfach([x, y[1], x2, y2[1]]).plot_line(ax=ax, ax2=ax2_1, color="r", label="Det2", label2="l2",color2="r")
Plot_einfach([x, y[2], x2, y2[2]]).plot_line(ax=ax, ax2=ax2_1, color="g", label="Det3", label2="l3",color2="g")


Plot_einfach([x,y[0]]).plot_line(color="b", ymin=ymin, ymin2=ymin2, xmin=0, xmin2=0, ymax=ymax, ymax2=ymax2, color2="b", label="Det1", label2="l1")
Plot_einfach([x,y[1]]).plot_line(color="r", ymin=ymin, ymin2=ymin2, xmin=0, xmin2=0, ymax=ymax, ymax2=ymax2, color2="r", label="Det2", label2="l2")

#plt.show()

#x array für variierendem emax


"""
        x_log = kwargs.get("log_x", False)  # Logarithmische x-Achse
        y_log = kwargs.get("log_y", False)  # Logarithmische y-Achse
        xlabel = kwargs.get("xlabel", "Energie [keV]")  # Beschriftung der x-Achse
        ylabel = kwargs.get("ylabel", "y_data")  # Beschriftung der y-Achse
        Name = kwargs.get("label", "label")  # Label
        color = kwargs.get("color", "blue")
        linewidth = kwargs.get("linewidth", 2) 
"""
#Plot_einfach([x,y[0],z]).plot_scatter()
#Plot_einfach([x,y[1]]).plot_scatter()
#Plot_einfach([x,y[1]]).plot_line()


#print(x,y,z)
#EmKi = call_class_with_config(Calc_I,"Emax=5.8000e+02, P1=[39]")
#print(EmKi.Röhre.Countrate_gesamt)
