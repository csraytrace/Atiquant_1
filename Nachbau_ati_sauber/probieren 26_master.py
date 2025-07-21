from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from Nachbau_ati_sauber.Calc_I import Calc_I

Ki=Calc_I(Konzentration=[1], P1=["Pb"], Übergänge=[0])
print(Ki.L3_M5())
# Anfangswerte für x1 und x2


Emax = 40
Ele = "pb"
step = 0.01

x_Ele = Element(Element = Ele, Emax = Emax, step = step)
Tube = Röhre(Emax = Emax, step = step)

print(x_Ele.Kanten())
for index, i in enumerate(Tube.Countrate_gesamt[0]):
    if (x_Ele.Kanten()[3][1] < i):
        break
x1_init, x2_init = Tube.Countrate_gesamt[0][index], Emax
# Berechnung von Sij_L3 für die gesamte Energieliste
Sij_L3 = np.array([x_Ele.S_ij("L3", Energie) for Energie in Tube.Countrate_gesamt[0]])

# Plot-Erstellung
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)  # Platz für die Slider lassen

line, = ax.plot(Tube.Countrate_gesamt[0][index:], 
                Tube.Countrate_gesamt[1][index:] * Sij_L3[index:] * x_Ele.tau[1][index:], zorder=4)

vline1 = ax.axvline(x=x1_init, color='r', linestyle='--', label=f'x1 = {x1_init}')
vline2 = ax.axvline(x=x2_init, color='b', linestyle='--', label=f'x2 = {x2_init}')



x = Tube.Countrate_gesamt[0][index:]
y = Tube.Countrate_gesamt[1][index:] * Sij_L3[index:] * x_Ele.tau[1][index:]
mask = (x >= x1_init) & (x <= x2_init)

# Fläche initial zeichnen
fill = ax.fill_between(x[mask], y[mask], color="orange", alpha=0.3)


# Slider für x1
ax_slider1 = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider1 = Slider(ax_slider1, 'x1', Tube.Countrate_gesamt[0][index], Emax, valinit=x1_init, valstep=step)

# Slider für x2
ax_slider2 = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider2 = Slider(ax_slider2, 'x2', Tube.Countrate_gesamt[0][index], Emax, valinit=x2_init, valstep=step)

# Funktion zur Aktualisierung des Plots
def update(val):
    x1 = slider1.val
    x2 = slider2.val
    
    # Update der vertikalen Linien
    vline1.set_xdata([x1])
    vline2.set_xdata([x2])
    vline1.set_label(f'x1 = {x1:.2f}')
    vline2.set_label(f'x2 = {x2:.2f}')


    global fill
    fill.remove()
    mask = (x >= x1) & (x <= x2)
    fill = ax.fill_between(x[mask], y[mask], color="orange", alpha=0.3)




    ax.legend()
    print(x2)
    
    # Neu berechnen und aktualisieren
    Summe = (Tube.Countrate_gesamt[1][index:] * Sij_L3[index:] * x_Ele.tau[1][index:]).sum()
    Summe2 = (Tube.Countrate_gesamt[1][int(x1/step - 1):int(x2/step - 1)] * 
              Sij_L3[int(x1/step - 1):int(x2/step - 1)] * 
              x_Ele.tau[1][int(x1/step - 1):int(x2/step - 1)]).sum()
    
    ax.set_title(f'{Summe2/Summe*100:.2f}%')
    fig.canvas.draw_idle()

# Verbinde die Slider mit der Update-Funktion
slider1.on_changed(update)
slider2.on_changed(update)

ax.set_xlabel('Energie [keV]')
ax.set_ylabel('Intensität * Tau_L3')
ax.set_yscale('log')
ax.legend()

plt.show()
