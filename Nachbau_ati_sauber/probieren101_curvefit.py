import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach

# Definiere eine Power-Law-Funktion: f(x) = a * x^b


Plot = True
x=(1.3490427098674522, 2.4476410523962135, 2.0423499059862698)
x=(2.079410197193107, 5.044247217780449, 3.071635561514673)#spinat 1


x=(2.2653956834532374, 6.068324781052258, 3.293654935984644)#1515
#x=(1.0389662560257098, 1.6921038685744567, 1.7687744371039504)#1486
x=(1.1299462628236443, 2.080150281778334, 2.010006791940231)#Klaudia
x=(1.1130289532293987, 2.076736049338789, 1.9686803162375837)#621
x=(0.492, 0.503370340999207, 0.9850872938894277)#1412
x=(1.390030607783122, 2.8014170723478093, 2.2560426832741567)#1646
x=(1.322594688724423, 2.51064879164238, 2.180638379204893)#SL3 IAEA
x=(1.2260778128286014, 2.2193287996903854, 2.041129297003236)#1633A
def power_law(x, a, b):
    return a * np.power(x, b)

def Z_ber(a,b,x):
    return (x/a)**(1/b)



x_data = np.array([6.764105747271824,6.675959047736525,  10.80458010185401, 13,10.655788151261717,22, 23,5.509237711718639,14,12.040593318088916])
max_ratio = [0.5192817972757827, 0.47087781731909845, 0.8507081495240306, 0.9724480578139115, 0.7878248487006052, 3.1619365609348913, 3.3859424920127794, 0.343804537521815, 0.942423030787685, 0.8565168653826557]
area_ratio = [0.15485595365578395, 0.14631553120143945, 0.3796465669301627, 0.5182779478316906, 0.3347508392119637, 4.732582503928758, 4.441867954911433, 0.07762063319984955, 0.4939948998881837, 0.43569176861789294]
area_ratio_mitback = [0.3666474983067125, 0.3500592647976667, 0.528063767483879, 0.5963138984251384, 0.49461529435048135, 1.522612791679146, 1.530709052164521, 0.28961559201910486, 0.5802744962129751, 0.5555957159434626]
z=['FLUX', 'CELLULOSE', 'SIO2', 'AL', 'SV J1', 'TI', 'V', 'HWC', 'SI', '3SI9HWC']
max_ratio = [1.9257366717765287, 2.123693160347651, 1.175491266375546, 1.0283325592196935, 1.2693176683235428, 0.31626187961985214, 0.29533874315908665, 2.9086294416243654, 1.0610946117946543, 1.1675193337299226]
area_ratio = [6.457614165890028, 6.83454443823365, 2.634028823402882, 1.9294666195690569, 2.9872964690815955, 0.2113011234711384, 0.22513051044083526, 12.883172408878755, 2.0243123972056214, 2.2952005799242268]
area_ratio_mitback =[2.7274153093047087, 2.8566591447822334, 1.8937106871861427, 1.6769691309241563, 2.021773308310612, 0.6567657946031008, 0.6532920143027413, 3.4528527729751297, 1.7233223354227432, 1.7998698897486818]



# Führe den Curve Fit für jeden Datensatz mit der Power-Law-Funktion durch:
popt_max, _ = curve_fit(power_law, x_data, max_ratio)
popt_area, _ = curve_fit(power_law, x_data, area_ratio)
popt_area_back, _ = curve_fit(power_law, x_data, area_ratio_mitback)


# Erzeuge einen feinen x-Vektor zum Plotten der Fit-Kurven
x_fit = np.linspace(np.min(x_data), np.max(x_data), 100)

# Berechne die Fit-Kurven
y_fit_max = power_law(x_fit, *popt_max)
y_fit_area = power_law(x_fit, *popt_area)
y_fit_area_back = power_law(x_fit, *popt_area_back)

# Plot für max_ratio:
plt.figure()
#plt.scatter(x_data, max_ratio, label="max_ratio", color='blue')
Plot_einfach([x_data,max_ratio,z], xy_format=True).plot_scatter(ylabel="Geometriefaktor")
plt.plot(x_fit, y_fit_max, 'r-', label=f"Fit: a={popt_max[0]:.2e}, b={popt_max[1]:.2f}")
plt.plot(x_fit, power_law(x_fit, 55.9,-2.12), 'g-', label=f"Fit: a={55.9:.2e}, b={-2.12:.2f} ganze Z modelliert")
plt.plot(x_fit, power_law(x_fit, 27.6,-1.39), 'b-', label=f"Fit: a={27.6:.2e}, b={-1.39:.2f}  Z 1-30 modelliert")
#plt.plot(x_fit, power_law(x_fit, 194.823,-2.150), 'g-', label=f"Fit: a={194.823:.2e}, b={-2.150:.2f} ganze Z modelliert")
#plt.plot(x_fit, power_law(x_fit, 101.835,-1.469), 'b-', label=f"Fit: a={101.835:.2e}, b={-1.469:.2f}  Z 1-30 modelliert")
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für max_ratio")
plt.legend()
if Plot:
    plt.show()

# Plot für area_ratio:
plt.figure()
#plt.scatter(x_data, area_ratio, label="area_ratio", color='green')
Plot_einfach([x_data,area_ratio,z], xy_format=True).plot_scatter(ylabel="Geometriefaktor",color='green')
plt.plot(x_fit, y_fit_area, 'r-', label=f"Fit: a={popt_area[0]:.2e}, b={popt_area[1]:.2f}")
plt.plot(x_fit, power_law(x_fit, 55.9,-2.12), 'g-', label=f"Fit: a={55.9:.2e}, b={-2.12:.2f} ganze Z modelliert")
plt.plot(x_fit, power_law(x_fit, 27.6,-1.39), 'b-', label=f"Fit: a={27.6:.2e}, b={-1.39:.2f}  Z 1-30 modelliert")
#plt.plot(x_fit, power_law(x_fit, 194.823,-2.150), 'g-', label=f"Fit: a={194.823:.2e}, b={-2.150:.2f} ganze Z modelliert")
#plt.plot(x_fit, power_law(x_fit, 101.835,-1.469), 'b-', label=f"Fit: a={101.835:.2e}, b={-1.469:.2f}  Z 1-30 modelliert")
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für area_ratio")
plt.legend()
if Plot:
    plt.show()

# Plot für area_ratio_mitback:
plt.figure()
#plt.scatter(x_data, area_ratio_mitback, label="area_ratio_mitback", color='purple')
Plot_einfach([x_data,area_ratio_mitback,z], xy_format=True).plot_scatter(ylabel="Geometriefaktor",color='purple')
plt.plot(x_fit, y_fit_area_back, 'r-', label=f"Fit: a={popt_area_back[0]:.2e}, b={popt_area_back[1]:.2f}")
plt.plot(x_fit, power_law(x_fit, 55.9,-2.12), 'g-', label=f"Fit: a={55.9:.2e}, b={-2.12:.2f} ganze Z modelliert")
plt.plot(x_fit, power_law(x_fit, 27.6,-1.39), 'b-', label=f"Fit: a={27.6:.2e}, b={-1.39:.2f}  Z 1-30 modelliert")
#plt.plot(x_fit, power_law(x_fit, 194.823,-2.150), 'g-', label=f"Fit: a={194.823:.2e}, b={-2.150:.2f} ganze Z modelliert")
#plt.plot(x_fit, power_law(x_fit, 101.835,-1.469), 'b-', label=f"Fit: a={101.835:.2e}, b={-1.469:.2f}  Z 1-30 modelliert")
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für area_ratio_mitback")
plt.legend()
if Plot:
    plt.show()



print(Z_ber(popt_max[0],popt_max[1], x[0]))
print(Z_ber(popt_area[0],popt_area[1], x[1]))
print(Z_ber(popt_area_back[0],popt_area_back[1], x[2]))

#für 20.2, auch 19.4
plt.plot(x_fit, power_law(x_fit, 55.9,-2.12), 'g-', label=f"Fit: a={55.9:.2e}, b={-2.12:.2f} ganze Z modelliert")
plt.plot(x_fit, power_law(x_fit, 27.6,-1.39), 'b-', label=f"Fit: a={27.6:.2e}, b={-1.39:.2f}  Z 1-30 modelliert")
#Gefundene Parameter: a = 55.933, b = -2.119
#Gefundene Parameter: a = 27.646, b = -1.393
#für 40 kV
#Gefundene Parameter: a = 194.823, b = -2.150
#Gefundene Parameter: a = 101.835, b = -1.469
plt.plot(x_fit, power_law(x_fit, 194.823,-2.150), 'g-', label=f"Fit: a={194.823:.2e}, b={-2.150:.2f} ganze Z modelliert")
plt.plot(x_fit, power_law(x_fit, 101.835,-1.469), 'b-', label=f"Fit: a={101.835:.2e}, b={-1.469:.2f}  Z 1-30 modelliert")
