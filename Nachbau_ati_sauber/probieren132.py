import matplotlib.pyplot as plt

def bracket(ax, x, y1, y2, text=None, direction='right', color='k', bracket_length=0.15, text_offset=0.05, **kwargs):
    # Linke oder rechte Klammer zeichnen (horizontal versetzt)
    sign = 1 if direction == 'right' else -1

    # Obere und untere kurze Linie
    ax.plot([x, x + sign*bracket_length], [y1, y1], color=color, lw=2)
    ax.plot([x, x + sign*bracket_length], [y2, y2], color=color, lw=2)
    # Verbindungslinie
    ax.plot([x, x], [y1, y2], color=color, lw=2)

    # Optional Text daneben
    if text:
        ax.annotate(
            text,
            xy=(x + sign*(bracket_length + text_offset), (y1+y2)/2),
            va='center', ha='left' if direction == 'right' else 'right',
            color=color, rotation=90, **kwargs
        )

# Beispiel
if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(5, 4))
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 2, 5, 3]
    ax.plot(x, y)

    # Bracket zwischen y=2 und y=5 bei x=4
    bracket(ax, x=4.2, y1=2, y2=5, text="Mein Bereich", direction='right', color='red', fontsize=12)
    # Optional auf linker Seite:
    # bracket(ax, x=0.8, y1=1, y2=4, text="Links", direction='left', color='blue', fontsize=10)

    plt.show()
