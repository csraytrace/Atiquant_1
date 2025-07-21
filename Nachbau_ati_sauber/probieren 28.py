
def add_arrays(arrays):
    return [
        [] if len(arrays[0][i]) == 0 else [
            sum(arr[i][j] for arr in arrays)
            for j in range(len(arrays[0][i]))
        ]
        for i in range(len(arrays[0]))
    ]

def add_arrays_with_multipliers(arrays, multipliers):
    return [
        [] if len(arrays[0][i]) == 0 else [
            sum(multipliers[idx] * arr[i][j] for idx, arr in enumerate(arrays))
            for j in range(len(arrays[0][i]))
        ]
        for i in range(len(arrays[0]))
    ]

# Beispielarrays
a = [
    [[], [620.5059485713638, 620.5059485713638], [620.5059485713638, 620.5059485713638]],
    [[], [521.2934042290325, 521.2934042290325], [521.2934042290325, 521.2934042290325]],
    [[], [521.2934042290325, 521.2934042290325], [521.2934042290325, 521.2934042290325]]
]

# Funktion aufrufen mit Multiplikatoren
multipliers = [1, 1, 1]
result = add_arrays_with_multipliers(a, multipliers)
print(result)
