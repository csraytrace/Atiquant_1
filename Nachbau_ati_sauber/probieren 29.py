# Funktion, die dynamisch die ersten vier Werte von beliebig vielen Arrays mit Multiplikatoren addiert
def add_first_four_with_concentration(arrays, Konzentration):
    result = []
    for i in range(len(arrays[0])):  # Durchlaufe die Subarrays
        summed_values = [
            sum(Konzentration[idx] * arr[i][j] for idx, arr in enumerate(arrays)) for j in range(4)
        ]  # Summe der ersten 4 Werte multipliziert mit den Multiplikatoren
        result.append(summed_values)
    return result

# Beispielarrays
a = [
    [[56264.966689877765, 0.05648315043155889, 0.05573784299882869, 0.05573784299882869], [555.332854131047, 0.245556071784219, 0.12965007736149098, 0.12965007736149098], [555.332854131047, 0.245556071784219, 0.12965007736149098, 0.12965007736149098]],
    [[242174.8556396109, 0.024805481659265938, 0.02476263745068523, 0.02476263745068523], [5401.1067233563745, 4536347.446418513, 47936099.663334765, 47936099.663334765], [5401.1067233563745, 4536347.446418513, 47936099.663334765, 47936099.663334765]],
    [[242174.8556396109, 0.024805481659265938, 0.02476263745068523, 0.02476263745068523], [5401.1067233563745, 4536347.446418513, 47936099.663334765, 47936099.663334765], [5401.1067233563745, 4536347.446418513, 47936099.663334765, 47936099.663334765]]
]

# Multiplikatoren
multipliers = [1, 2, 3]

# Funktion aufrufen
result = add_first_four_with_concentration(a, multipliers)
print(result)
