from Nachbau_ati_sauber.Element import Element






Ele=Element(Element="K")

print(Ele.K_gemittel_ubergang())
Energie=Ele.K_gemittel_ubergang()
#x.S_ij(" K", Energie)
print(Ele.Massenabsorptionskoeffizient(Energie))
print(Ele.S_ij(" K", Energie))

Element_x = Element(Element="Ru")
print(Element_x.Löcherübertrag_L3_Energie(17.44))
print(Element_x.Löcherübertrag_L3_Energie(22.5))


x=Element(Element="Pb")
print(x.Massenabsorptionskoeffizient(15.236)[1][0]/x.Get_cm2g())
