from Nachbau_ati_sauber.Element import Element
import numpy as np



x_data = np.tile(np.linspace(0, 1, 10), 10)
y_data = np.repeat(np.linspace(0, 1, 10), 10)

print(x_data, y_data)
#for i in [26,28,29,30,82]:
  #  x_ele = Element(Element = i)
  #  print(x_ele.Get_Elementsymbol())
