import os

# Suchparameter
SUCHWORT = "Rh-Röhrenspe"  # hier einmal
ORDNER = "C:\\Users\\julia\\OneDrive\\Dokumente\\A_Christian\\Masterarbeit\\Nachbau_neu"  # z.B. "C:/Users/julia/OneDrive/Dokumente/A_Christian/Masterarbeit/Nachbau_neu"
#C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Nachbau_neu

for root, dirs, files in os.walk(ORDNER):
    for fname in files:
        # Hier kannst du z.B. nur nach .py-Dateien suchen:
        # if not fname.endswith('.py'): continue
        try:
            with open(os.path.join(root, fname), encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if SUCHWORT in line:
                        print(f"{os.path.join(root, fname)}:{i}: {line.strip()}")
        except Exception as e:
            print(f"Fehler bei Datei {fname}: {e}")
