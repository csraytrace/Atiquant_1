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

