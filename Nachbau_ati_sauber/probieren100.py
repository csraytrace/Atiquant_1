import numpy as np

def _enforce_non_increasing(seg):
    """
    Hilfsfunktion: Erzwingt, dass das übergebene eindimensionale Segment seg
    nicht ansteigt (also monoton nicht steigend ist).

    Falls ein Wert (nach dem Start) größer ist als der vorherige, wird das betroffene
    Intervall von der letzten gültigen Stelle bis zu dem Punkt, an dem wieder ein
    kleinerer (oder gleicher) Wert auftritt, linear interpoliert.

    Parameters:
      seg : 1D-Array (numpy.array)

    Returns:
      Das korrigierte Segment.
    """
    seg = seg.copy()
    i = 0
    n = len(seg)
    while i < n - 1:
        if seg[i+1] <= seg[i]:
            i += 1
        else:
            # Verletzung: seg[i+1] > seg[i]
            start = i
            j = i + 1
            while j < n and seg[j] > seg[start]:
                j += 1
            if j >= n:
                j = n - 1
            # Lineare Interpolation von seg[start] bis seg[j]
            for k in range(start + 1, j):
                seg[k] = seg[start] + (seg[j] - seg[start]) * (k - start) / (j - start)
            i = j
    return seg

def Raenderkorrektur(array):
    """
    Korrigiert die Ränder eines Arrays anhand eines globalen Peaks.

    Es wird zunächst das globale Maximum gesucht. Anschließend wird:
      - Im linken Bereich (von Index 0 bis zum globalen Maximum)
        der erste Minimalwert (z. B. 624) bestimmt. Ab diesem Index bis zum
        Maximum werden alle Werte auf diesen Minimalwert gesetzt.
      - Im rechten Bereich (vom globalen Maximum bis zum Ende)
        der erste Minimalwert (z. B. 1767) bestimmt. Ab diesem Index werden
        alle folgenden Werte auf diesen Minimalwert gesetzt.

    So wird sichergestellt, dass an den Rändern (links und rechts) nach Erreichen
    des minimalen Wertes keine Werte mehr „wieder ansteigen“.

    Parameters:
      array : 1D-Array (numpy.array)

    Returns:
      Das Array mit korrigierten Rändern.
    """
    corrected = array.copy()
    max_idx = np.argmax(array)

    # Linker Bereich: von 0 bis max_idx
    left_region = array[:max_idx+1]
    left_min = left_region.min()
    # Ersten Index finden, an dem der Minimalwert auftritt:
    left_min_idx = np.where(left_region == left_min)[0][0]
    # Ab diesem Index bis zum globalen Maximum wird der Wert konstant auf left_min gesetzt:
    corrected[0:left_min_idx] = left_min

    # Rechter Bereich: von max_idx bis Ende
    right_region = array[max_idx:]
    right_min = right_region.min()
    right_min_idx = np.where(right_region == right_min)[0][0] + max_idx
    corrected[right_min_idx:] = right_min

    return corrected

def enforce_monotonicity_from_peak(arr):
    """
    Sucht das globale Maximum in einem eindimensionalen Array und erzwingt:
      - Links vom Maximum ein monoton ansteigendes Verhalten, indem zuerst das
        linke Segment umgekehrt wird, _enforce_non_increasing darauf angewandt
        und das Ergebnis anschließend zurückgedreht wird.
      - Rechts vom Maximum ein monoton abfallendes Verhalten mittels
        _enforce_non_increasing.

    Anschließend wird mit Raenderkorrektur dafür gesorgt, dass an den Rändern,
    sobald ein Minimalwert erreicht wurde (z. B. 624 links oder 1767 rechts),
    alle folgenden Werte auf diesen Minimalwert gesetzt werden.

    Beispiel:
      [3, 2, 2.5, 2]  ->  [3, 2, 2, 2]
      [4, 3, 3.5, 3.5, 2]  ->  [4, 3, 2.6667, 2.3333, 2]

    Parameters:
      arr : 1D-Array (z.B. numpy.array)

    Returns:
      Das korrigierte Array.
    """
    arr = np.array(arr)
    corrected = arr.copy()
    max_idx = np.argmax(arr)

    # Linker Teil: Von Index 0 bis zum Maximum
    left_seg = corrected[:max_idx+1]
    # Umkehren, damit wir ein monoton nicht-steigendes Segment erzwingen:
    left_seg_rev = left_seg[::-1]
    left_seg_rev_corr = _enforce_non_increasing(left_seg_rev)
    corrected[:max_idx+1] = left_seg_rev_corr[::-1]

    # Rechter Teil: Vom Maximum bis zum Ende
    right_seg = corrected[max_idx:]
    right_seg_corr = _enforce_non_increasing(right_seg)
    corrected[max_idx:] = right_seg_corr

    # Ränderkorrektur: Klammern die Randbereiche ab, sodass nach dem Erreichen
    # des Minimalwertes (links bzw. rechts) keine Werte mehr darüber liegen.
    corrected = Raenderkorrektur(corrected)

    return corrected

# Testbeispiele

# Beispiel 1:
data1 = np.array([3, 2, 2.5, 2])
print("Original data1:  ", data1)
print("Korrigiert data1:", enforce_monotonicity_from_peak(data1))
# Erwartetes Ergebnis: [3, 2, 2, 2]

# Beispiel 2:
data2 = np.array([4, 3, 3.5, 3.5, 2])
print("Original data2:  ", data2)
print("Korrigiert data2:", enforce_monotonicity_from_peak(data2))
# Erwartetes Ergebnis: [4, 3, ca. 2.6667, ca. 2.3333, 2]

# Beispiel mit dem größeren Array (Ausschnitt)
data3 = np.array([758, 775, 793, 810, 828, 845, 863, 880, 898, 915, 933, 907, 873, 838,
                  784, 755, 693, 742, 624, 698, 676, 686, 665, 708, 667, 646, 656, 629,
                  645, 643, 658, 706, 669, 708, 688, 731, 703, 715, 713, 752, 673, 771,
                  795, 760, 798, 792, 824, 807, 783, 776, 821, 783, 753, 801, 753, 788,
                  720, 723, 807, 735, 716, 679, 712, 707, 740, 725, 691, 692, 695, 735,
                  694, 752, 773, 735, 785, 805, 832, 891, 943, 993, 1065, 1123, 1249, 1291,
                  1350, 1412, 1440, 1447, 1510, 1529, 1459, 1404, 1330, 1280, 1177, 1061,
                  1017, 990, 958, 880, 896, 793, 841, 807, 766, 720, 791, 773, 779, 800,
                  795, 805, 789, 774, 787, 812, 831, 812, 786, 817, 789, 788, 785, 777,
                  807, 875, 821, 891, 828, 855, 873, 862, 824, 878, 878, 863, 873, 874,
                  906, 848, 858, 864, 818, 867, 799, 791, 883, 850, 867, 915, 830, 874,
                  884, 887, 884, 833, 883, 805, 880, 833, 938, 842, 887, 932, 910, 936,
                  848, 937, 928, 931, 911, 914, 926, 976, 938, 972, 925, 1010, 997, 1004,
                  1053, 1089, 1128, 1112, 1104, 1037, 1065, 1090, 1002, 988, 1032, 1033,
                  1033, 1016, 966, 1032, 1053, 1060, 1034, 1012, 1063, 1028, 1103, 1056,
                  1006, 1055, 1053, 1055, 1024, 1075, 1045, 1080, 1089, 1109, 1138, 1089,
                  1115, 1137, 1135, 1158, 1190, 1155, 1185, 1149, 1189, 1276, 1278, 1292,
                  1347, 1366, 1437, 1405, 1418, 1520, 1505, 1531, 1549, 1621, 1570, 1687,
                  1780, 1783, 1973, 2035, 2063, 2253, 2399, 2508, 2642, 2829, 2985, 3158,
                  3349, 3566, 3835, 4106, 4203, 4449, 4711, 4881, 4948, 5139, 5288, 5338,
                  5353, 5398, 5416, 5496, 5410, 5150, 5137, 5103, 4819, 4768, 4400, 4302,
                  3937, 3747, 3565, 3368, 3200, 3014, 2795, 2598, 2358, 2273, 2118, 1999,
                  1933, 1887, 1767, 1821, 1863, 1815])
corrected_data3 = enforce_monotonicity_from_peak(data3)
#print("Erster Ausschnitt original:", data3[:20])
#print("Erster Ausschnitt korrigiert:", corrected_data3[:20])
#print("Letzter Ausschnitt original:", data3[-10:])
#print("Letzter Ausschnitt korrigiert:", corrected_data3[-10:])
print(corrected_data3)
