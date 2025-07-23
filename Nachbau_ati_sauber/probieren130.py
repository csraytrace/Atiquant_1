import numpy as np
import matplotlib.pyplot as plt
from Nachbau_ati_sauber.Element import Element
from Nachbau_ati_sauber.Röhre import Röhre
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from Nachbau_ati_sauber.Calc_I import Calc_I

from Nachbau_ati_sauber.Geoplot_klasse import Plot_einfach
import matplotlib.pyplot as plt

Emin=1.1
Emax=30
step=0.01
x_ele=Element(Element="Pb",step=step,Emax=Emax,Emin=Emin)
x,y=x_ele.Massenabsorptionskoeffizient_array()



print(x_ele.Kanten())
def bracket(ax, x, y1, y2, text=None, direction='left', color='k', bracket_length=0.15, text_offset=0.05,lw=1, **kwargs):
    # Linke oder rechte Klammer zeichnen (horizontal versetzt)
    sign = 1 if direction == 'right' else -1

    # Obere und untere kurze Linie
    ax.plot([x- bracket_length, x], [y1, y1], color=color, lw=lw)
    ax.plot([x- bracket_length, x], [y2, y2], color=color, lw=lw)
    # Verbindungslinie
    ax.plot([x- bracket_length, x- bracket_length], [y1, y2], color=color, lw=lw)
    # Optional Text daneben
    if text:
        ax.annotate(
            text,
            xy=(x + sign*(bracket_length + text_offset), (y1+y2)/2),
            va='center', ha='left' if direction == 'right' else 'right',
            color=color, rotation=90, **kwargs
        )


def line(ax, x, y1, y2, text=None, color='k', text_offset=0.1,lw=1, **kwargs):
    # Linke oder rechte Klammer zeichnen (horizontal versetzt)
    ax.plot([x, x], [y1, y2], color=color, lw=lw)

    # Optional Text daneben
    if text:
        ax.annotate(
            text,
            xy=(x + (text_offset), (y2+4)),
            va='center', ha='left',
            color="grey", rotation=0, fontsize=10, **kwargs
        )



K = np.array([x_ele.TauK(xi) for xi in x])
L1 = np.array([x_ele.TauL(xi) for xi in x])
L2 = np.array([x_ele.TauM(xi) for xi in x])
L3 = np.array([x_ele.TauN(xi) for xi in x])

colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:green",
    "tab:cyan",
    "tab:gray",
    "tab:brown"
]
sij=x_ele.S_ij("L1", 17)
sij2=x_ele.S_ij("L2", 17)
sij3=x_ele.S_ij("L3", 17)
print(sij,sij2,sij3)
print(1/sij,1/sij2,1/sij3)

start=int(15.861/step-x[0]/step+1)
L1_index=int(15.2/step-x[0]/step+1)
L2_index=int(13.035/step-x[0]/step+1)

#Plot_einfach([x,L1], xy_format=True).plot_line(ylabel="Tau",color=colors[1],label="Tau-K")
#Plot_einfach([x,y*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[4],label=r"$\mathrm{Tau} \cdot S_{iL_2}$")
#Plot_einfach([x,L2], xy_format=True).plot_line(ylabel="Tau",color=colors[2],label="Tau -K-L")
#Plot_einfach([x,L3], xy_format=True).plot_line(ylabel="Tau",color=colors[3],label="Tau -K-L-M",title="Pb-Massenabsorptionskoeffizient")
Plot_einfach([x,y], xy_format=True).plot_line(ylabel="Tau",color=colors[0],label=r"$\tau$",title="Pb-Massenabsorptionskoeffizient")
#Plot_einfach([x,y-y*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[5],label=r"$\mathrm{Tau} \cdot S_{iL_1}$")
Plot_einfach([x[start:],y[start:]-y[start:]*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[5],label=r"$\mathrm{\tau} - \mathrm{\tau} \cdot S_{iL_1}$")
Plot_einfach([x[start:],y[start:]-y[start:]*sij2-y[start:]*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[6],label=r"$\mathrm{\tau} - \mathrm{\tau} \cdot S_{iL_2} - \mathrm{\tau} \cdot S_{iL_1}$")
Plot_einfach([x[start:],y[start:]-y[start:]*sij3-y[start:]*sij2-y[start:]*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[7],label=r"$\mathrm{\tau}- \mathrm{\tau} \cdot S_{iL_3}- \mathrm{\tau} \cdot S_{iL_2}- \mathrm{\tau} \cdot S_{iL_1}$")


Plot_einfach([x[L1_index:start],L1[L1_index:start]-L1[L1_index:start]*sij2-L1[L1_index:start]*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[6], linestyle='--')
Plot_einfach([x[L2_index:start],L1[L2_index:start]-L1[L2_index:start]*sij3-L1[L2_index:start]*sij2-L1[L2_index:start]*sij], xy_format=True).plot_line(ylabel="Tau",color=colors[7], linestyle='--')

Energie=15.86
index=(int(Energie/step-x[0]/step+1))
print(y[index],y[index-1])

bracket(plt, x=Energie, y1=y[int(Energie/step-x[0]/step)], y2=y[int(Energie/step-x[0]/step+1)], text=r"$r_{iL_1}$", direction='left', color='black', fontsize=12)


Energie=15.2
index=(int(Energie/step-x[0]/step+1))
print(y[index],y[index-1])

bracket(plt, x=Energie, y1=y[int(Energie/step-x[0]/step-1)], y2=y[int(Energie/step-x[0]/step)], text=r"$r_{iL_2}$", direction='left', color='black', fontsize=12)


Energie=13.035
index=(int(Energie/step-x[0]/step+1))
print(y[index],y[index-1])

bracket(plt, x=Energie, y1=y[int(Energie/step-x[0]/step)], y2=y[int(Energie/step-x[0]/step+1)], text=r"$r_{iL_3}$", direction='left', color='black', fontsize=12)


Energie=18
index=(int(Energie/step-x[0]/step))
#y[start:]-y[start:]*sij
line(plt, x=Energie, y1=y[index], y2=y[index]-y[index]*sij, text=r"$\tau_{L_1}(E) = \tau(E) \cdot S_{iL_1}(E)$", color=colors[5])


Energie=18.2
index=(int(Energie/step-x[0]/step))
#y[start:]-y[start:]*sij
line(plt, x=Energie, y1=y[index]-y[index]*sij, y2=y[index]-y[index]*sij-y[index]*sij2, text=r"$\tau_{L_2}(E) = \tau(E) \cdot S_{iL_2}(E)$", color=colors[6])


Energie=18.4
index=(int(Energie/step-x[0]/step))
#y[start:]-y[start:]*sij
line(plt, x=Energie, y1=y[index]-y[index]*sij-y[index]*sij2, y2=y[index]-y[index]*sij-y[index]*sij2-y[index]*sij3, text=r"$\tau_{L_3}(E) = \tau(E) \cdot S_{iL_3}(E)$", color=colors[7])


plt.ylabel(r"$\tau$")


#Plot_einfach([x,y-y*sij3], xy_format=True).plot_line(ylabel="Tau",color=colors[5],label=r"$\mathrm{Tau} \cdot S_{iL_1}$")
plt.axvline(x=15.861, color='r', linestyle='-', label=r'gültig für E > 15.8 ($L_1$<E<K)')
plt.ylim(0, 200)
plt.xlim(12, 22)
plt.legend(loc="upper right",fontsize=8)
plt.title("Pb Massenabsorptionskoeffizient")
plt.savefig("C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Masterarbeit\\Pb_Massenabsorptionskoeffizient.png", dpi=600, bbox_inches='tight')
plt.show()

