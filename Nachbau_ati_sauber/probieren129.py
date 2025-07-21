import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Beispiel-Daten
x = np.linspace(13.0, 40.0, 540)
y = np.exp(-(x-20)**2 / 20) * 1e3  # Beispiel-Plot mit "Hügel"

step = 0.05
x1_init = 20
x2_init = 30

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.8)  # Platz für Slider/Button

line, = ax.plot(x, y, label="Intensität")
vline1 = ax.axvline(x=x1_init, color='r', linestyle='--', label=f'x1 = {x1_init}')
vline2 = ax.axvline(x=x2_init, color='b', linestyle='--', label=f'x2 = {x2_init}')
mask = (x >= x1_init) & (x <= x2_init)
fill = ax.fill_between(x[mask], y[mask], color="orange", alpha=0.3)

ax.set_xlabel('Energie')
ax.set_ylabel('Beiträge (Intensität)')
ax.set_yscale('log')
ax.legend()

# Slider für x1
ax_slider1 = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider1 = Slider(ax_slider1, 'x1', x[0], x[-1], valinit=x1_init, valstep=step)

# Slider für x2
ax_slider2 = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider2 = Slider(ax_slider2, 'x2', x[0], x[-1], valinit=x2_init, valstep=step)

def update(val):
    x1 = slider1.val
    x2 = slider2.val
    vline1.set_xdata([x1])
    vline2.set_xdata([x2])
    vline1.set_label(f'x1 = {x1:.2f}')
    vline2.set_label(f'x2 = {x2:.2f}')

    global fill
    fill.remove()
    mask = (x >= x1) & (x <= x2)
    fill = ax.fill_between(x[mask], y[mask], color="orange", alpha=0.3)

    ax.legend()
    Summe = y.sum()
    # Index-Berechnung wie bei dir
    idx1 = int(round((x1 - x[0]) / step))
    idx2 = int(round((x2 - x[0]) / step))
    Summe2 = y[idx1:idx2].sum()
    ax.set_title(f'{Summe2/Summe*100:.2f}%')
    fig.canvas.draw_idle()

slider1.on_changed(update)
slider2.on_changed(update)

# Button zum scharfen Export
ax_save = plt.axes([0.81, 0.925, 0.15, 0.045])
button = Button(ax_save, 'Scharf speichern')

def save_sharp_plot(event):
    x1 = slider1.val
    x2 = slider2.val
    mask = (x >= x1) & (x <= x2)
    Summe = y.sum()
    idx1 = int(round((x1 - x[0]) / step))
    idx2 = int(round((x2 - x[0]) / step))
    Summe2 = y[idx1:idx2].sum()

    # Neue Figure OHNE Slider/Buttons!
    fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=600)
    ax2.plot(x, y, label="Intensität")
    ax2.axvline(x=x1, color='r', linestyle='--', label=f'x1 = {x1:.2f}')
    ax2.axvline(x=x2, color='b', linestyle='--', label=f'x2 = {x2:.2f}')
    ax2.fill_between(x[mask], y[mask], color="orange", alpha=0.3)
    ax2.set_xlabel('Energie')
    ax2.set_ylabel('Beiträge (Intensität)')
    ax2.set_yscale('log')
    ax2.set_title(f'{Summe2/Summe*100:.2f}%')
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("mein_plot_scharf.png", dpi=600, bbox_inches='tight')
    plt.close(fig2)
    print("Plot scharf gespeichert!")

button.on_clicked(save_sharp_plot)

plt.show()
