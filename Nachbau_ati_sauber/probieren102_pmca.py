import re

def extract_fitareas(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Alle [result.*]-Sektionen (bis zum nächsten "[" oder Dateiende) extrahieren
    pattern = re.compile(r'\[result\.([^\]]+)\](.*?)(?=\n\[|$)', re.DOTALL)
    sections = pattern.findall(content)

    # Ergebnisse als Liste von (Sektion_Name, fitarea) Tupeln speichern
    fitareas = []
    for section_name, section_content in sections:
        # Sucht nach einer Zeile, die "fitarea = ..." enthält
        match = re.search(r'fitarea\s*=\s*([-\d\.eE]+)', section_content)
        if match:
            try:
                value = float(match.group(1))
                fitareas.append((section_name.strip(), value))
            except ValueError:
                continue
    return fitareas

def Ele(str):
    if str[1]==" ":
        return str[0]
    else:
        return str[0:2]

def Übergang_suche(str):
    Übergänge=["KL2","KL3", "L3M4","L3M5"]
    retar=[]
    for x in str:
        #print(x[0],len(x[0]))
        if any(übergang in x[0] for übergang in Übergänge) and "esc" not in x[0]:
        #if x[0] in Übergänge and len(x[0])<15:
            retar.append(x)
    return retar

def Gruppieren(text):
    Elemente=[]
    Übergänge=[]
    for x in text:
        str = Ele(x[0])
        if str not in Elemente:
            Elemente.append(str)
    for ele in Elemente:
        Über_append=[]
        for x in text:
            if x[0][0:len(ele)] == ele:
                if len(ele)==1:
                    if x[0][1]==" ":
                        Über_append.append(x)
                else:
                    Über_append.append(x)
        Übergänge.append(Über_append)
    for index, x in enumerate(Übergänge):
        Übergänge[index]=(Übergang_suche(x))
    return Elemente, Übergänge

def Übergang_fkt(Übergänge):
    K_über=[]
    L_über=[]
    for Über in Übergänge:
        if any(übergang in Über[0] for übergang in ["KL2","KL3"]):
            K_über.append(Über)
        if any(übergang in Über[0] for übergang in ["L3M4","L3M5"]):
            L_über.append(Über)
    #print(K_über,L_über)
    sum_k=0
    sum_l=0
    for x in K_über:
        sum_k += x[1]
    for x in L_über:
        sum_l += x[1]
    return sum_k,sum_l

def werte(Elemente,Übergänge):
    count=[]
    uber=[]
    for index,ele in enumerate(Elemente):
        x,y = Übergang_fkt(Übergänge[index])
        if x != 0:
            count.append((round(x),ele))
            uber.append(0)
        if y != 0:
            count.append((round(y),ele))
            uber.append(1)
    return count, uber


        #print(Übergang_fkt(Übergänge[index]))





if __name__ == "__main__":
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\pymca_dat\1570A.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\pymca_dat\1515.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\pymca_dat\SAMPLE_1.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\pymca_dat\1486.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\KLAUD\621NIST.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\KLAUD\1412NIST.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\KLAUD\1646.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\KLAUD\SL3IAEA.spe_1.1.1.1.fit'
    file_path = r'C:\Users\julia\OneDrive\Dokumente\A_Christian\Masterarbeit\Tracormessungen\Messung2025\KLAUD\1633A.spe_1.1.1.1.fit'

    result_array = extract_fitareas(file_path)
    #print(result_array)
    print(Gruppieren(result_array))
    x,y=Gruppieren(result_array)
    print(werte(x,y))
    print(werte(*Gruppieren(result_array)))

