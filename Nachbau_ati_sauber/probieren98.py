import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
# Definiere eine Power-Law-Funktion: f(x) = a * x^b
def power_law(x, a, b):
    return a * np.power(x, b)

# Beispiel-Daten:
x_data = np.array([14, 22, 23, 13, 10.80458010185401, 7.468644393629722, 10.655788151261717, 6.764105747271824])
max_ratio = 1/np.array([0.7469304229195088, 3.026666666666667, 3.218241042345277, 0.9171830985915493,
                        0.8260701889703047, 0.8186195826645265, 0.7390468870099923, 0.4541757443718228])
area_ratio = 1/np.array([0.4362716481805799, 3.8363943934267764, 3.558861246473455, 0.6851238887838094,
                         0.40696582596353315, 0.45120663924580495, 0.3691367351143465, 0.14620454802428984])
area_ratio_mitback = 1/np.array([0.49543374351672936, 2.047072967724036, 1.8401078790213832, 0.6539725532683279,
                                 0.47816201859229746, 0.5099504902436657, 0.4566322568621157, 0.2847602283031952])

area_ratio_mitback = 1/np.array([0.2973146345779508, 0.7606646198302329, 0.697009674582234, 0.3431714588638279,
                                 0.3084776686411237, 0.32040475174277994, 0.2825002551158226, 0.19706072961952853])
z=["Si","Ti", "V", "Al","SiO2", "Si+HWC", "SV J1", "Flux"]


x_data = np.array([ 22, 23, 13, 10.80458010185401, 10.655788151261717, 6.764105747271824])
max_ratio = 1/np.array([ 3.026666666666667, 3.218241042345277, 0.9171830985915493,
                        0.8260701889703047,  0.7390468870099923, 0.4541757443718228])
area_ratio = 1/np.array([ 3.8363943934267764, 3.558861246473455, 0.6851238887838094,
                         0.40696582596353315,  0.3691367351143465, 0.14620454802428984])
area_ratio_mitback = 1/np.array([ 2.047072967724036, 1.8401078790213832, 0.6539725532683279,
                                 0.47816201859229746, 0.4566322568621157, 0.2847602283031952])


#area_ratio_mitback = np.array([0.2973146345779508, 0.7606646198302329, 0.697009674582234, 0.3431714588638279, 0.3084776686411237, 0.32040475174277994, 0.2825002551158226, 0.19706072961952853])
area_ratio_mitback = 1/np.array([ 0.7606646198302329, 0.697009674582234, 0.3431714588638279, 0.3084776686411237, 0.2825002551158226, 0.19706072961952853])
z=["Ti", "V", "Al","SiO2", "SV J1", "Flux"]





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
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für max_ratio")
plt.legend()
plt.show()

# Plot für area_ratio:
plt.figure()
#plt.scatter(x_data, area_ratio, label="area_ratio", color='green')
Plot_einfach([x_data,area_ratio,z], xy_format=True).plot_scatter(ylabel="Geometriefaktor",color='green')
plt.plot(x_fit, y_fit_area, 'r-', label=f"Fit: a={popt_area[0]:.2e}, b={popt_area[1]:.2f}")
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für area_ratio")
plt.legend()
plt.show()

# Plot für area_ratio_mitback:
plt.figure()
#plt.scatter(x_data, area_ratio_mitback, label="area_ratio_mitback", color='purple')
Plot_einfach([x_data,area_ratio_mitback,z], xy_format=True).plot_scatter(ylabel="Geometriefaktor",color='purple')
plt.plot(x_fit, y_fit_area_back, 'r-', label=f"Fit: a={popt_area_back[0]:.2e}, b={popt_area_back[1]:.2f}")
plt.xlabel("x")
plt.ylabel("Geometriefaktor")
plt.title("Power-Law Fit für area_ratio_mitback")
plt.legend()
plt.show()
