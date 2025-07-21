#from Nachbau_ati_sauber.probieren35 import DreidimensionalerPlot
from Nachbau_ati_sauber.probieren7 import DreidimensionalerPlot
import numpy as np
from Nachbau_ati_sauber.Calc_I import Calc_I

x_extra = [
    0.6396691894568102, 0.6396692043579714, 0.6396691894568102,
    0.6787265638988723, 0.6787265788000335, 0.6787265638988723,
    0.6798907152370077, 0.6798907301381689, 0.6798907152370077,
    0.679891790337448, 0.6798918052386091, 0.679891790337448,
    0.771726986557116, 0.7028505893920739, 0.6856314901008134,
    0.6813267152779983, 0.6802505215722945, 0.6802505364734557,

]
y_extra = [
    0.36033081054318983, 0.36033081054318983, 0.360330825444351,
    0.36033081081624363, 0.36033081081624363, 0.3603308257174048,
    0.36033081078851836, 0.36033081078851836, 0.36033082568967956,
    0.360330882882791, 0.360330882882791, 0.3603308977839522,
    0.409001949780284, 0.37249864960797197, 0.36337282456489395,
    0.36109136830412447, 0.3605210042389321, 0.3605210042389321,

]



z_extra = [
    508.4523533529642, 508.4519654619239, 508.4530419482081,
    0.4034339327596957, 0.40342360503473074, 0.40345338663459684,
    6.708815607683847e-06, 6.70057742390656e-06, 6.724718711789533e-06,
    6.447155900536862e-06, 6.44722180409059e-06, 6.447390421966439e-06,
    6.447159764362946e-06, 6.4471561906402396e-06, 6.447155918597677e-06,
    6.4471559042823965e-06, 6.44715590035563e-06, 6.447221574807401e-06,

]


K = Calc_I(Element_Probe=30, Konzentration=[847554,477434], P1 = [29,30], Fensterdicke_det=12, Messzeit=300, Emax=30)


Geo = 4 * 10**-7 * 61 * 1.0066

op_Konz = K.Minimierung_sqrt(Geo)

x_data = np.tile(np.linspace(0, 1, 10), 10)
y_data = np.repeat(np.linspace(0, 1, 10), 10)

x_data = np.tile(np.linspace(0.3, 3, 50), 10)
y_data = np.repeat(np.linspace(0.3, 3, 50), 10)

unten = 0.8
oben = 1.2
anzahl = 12

x_data = np.tile(np.linspace(op_Konz[0]*unten, op_Konz[0] * oben, anzahl), anzahl)
y_data = np.repeat(np.linspace(op_Konz[1]*unten, op_Konz[1] * oben, anzahl), anzahl)

non_zero_indices = (x_data != 0) & (y_data != 0)  # Nur die Werte behalten, die in x und y nicht Null sind
x_data_filtered = x_data[non_zero_indices]
y_data_filtered = y_data[non_zero_indices]


# Berechne z_data basierend auf den gefilterten x_data und y_data
z_data_filtered = [K.Kosten([x_data_filtered[i], y_data_filtered[i]], Geo) for i in range(len(x_data_filtered))]
#z_data_filtered = [K.Kosten_2([x_data_filtered[i], y_data_filtered[i]], Geo) for i in range(len(x_data_filtered))]


# Instanziere die Klasse
plotter = DreidimensionalerPlot(title="Hyperfläche", xlabel="Konzentration Element 1", ylabel="Konzentration Element 2", zlabel="Chi Square")

# Streuplot
#plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='scatter')

#plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='line')

x_line = np.linspace(op_Konz[0]*unten, op_Konz[0]*oben, anzahl)
y_line = np.linspace(op_Konz[1]*unten, op_Konz[1] * oben, anzahl)
z_line = np.full(anzahl, K.Kosten(op_Konz, Geo))


plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='linear', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra))
plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='cubic', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra))
plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='nearest', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra))

plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='linear', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra), log_scale=True)
plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='cubic', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra), log_scale=True)
plotter.plot(x_data_filtered, y_data_filtered, z_data_filtered, plot_type='surface', interpolation_method='nearest', line_coords=(x_line, y_line, z_line),
                 extra_points=(x_extra, y_extra, z_extra), log_scale=True)


