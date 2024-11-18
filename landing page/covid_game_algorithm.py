#algoritmo che calcola la probabilità di contagio

def calcola_probabilita(df, regione, settimana, sintomi, durata_sintomi, gravita_sintomi, contatto_con_positivi):
    
    # Filtra il DataFrame per la regione e settimana specifiche
    dati_selezionati = df[(df['denominazione_regione'] == regione) & (df['data'] == settimana)]
    
    # Estrazione dei dati necessari al calcolo
    nuovi_casi = dati_selezionati['nuovi_positivi'].values[0]
    tamponi_settimanali = dati_selezionati['tamponi_settimanali'].values[0]
    tamponi_positivi_settimanali = dati_selezionati['tamponi_positivi_settimanali'].values[0]

    # Calcola la media storica dei nuovi casi e del rapporto positivi/tamponi per la regione
    media_nuovi_casi = df[df['denominazione_regione'] == regione]['nuovi_positivi'].mean()
    media_rapporto_positivi = (df[df['denominazione_regione'] == regione]['tamponi_positivi_settimanali'] /
                               df[df['denominazione_regione'] == regione]['tamponi_settimanali']).mean()
    
    # 1) Moltiplicatore in base ai sintomi
    if len(sintomi) == 0:
        sintomi_moltiplicatore = 0.1
    elif len(sintomi) <= 2:
        sintomi_moltiplicatore = 1
    else:
        sintomi_moltiplicatore = 1.2

    # 2) Moltiplicatore in base alla durata dei sintomi
    if durata_sintomi < 3:
        durata_moltiplicatore = 0.7  # Sintomi di breve durata, meno probabile COVID
    elif durata_sintomi < 7:
        durata_moltiplicatore = 1.4  # Sintomi di durata moderata, probabilità standard
    elif durata_sintomi <= 10:
        durata_moltiplicatore = 1.6
    else:
        durata_moltiplicatore = 2 # Sintomi di lunga durata, più probabile COVID

    # 3) Moltiplicatore in base alla gravità dei sintomi
    if gravita_sintomi == "Low":
        gravita_moltiplicatore = 0.8  # Sintomi lievi, meno probabile COVID
    elif gravita_sintomi == "Medium":
        gravita_moltiplicatore = 1.0  # Sintomi moderati, probabilità standard
    else:
        gravita_moltiplicatore = 1.3  # Sintomi severi, più probabile COVID

    # 4. Moltiplicatore in base ai contatti con positivi confermati
    if contatto_con_positivi:
        contatto_moltiplicatore = 2 
    else:
        contatto_moltiplicatore=0.9

    if nuovi_casi > media_nuovi_casi * 5.0:
        casi_moltiplicatore = 1.6  # Molto più alti della media
    elif nuovi_casi > media_nuovi_casi * 3.0:
        casi_moltiplicatore = 1.35  # Molto alti rispetto alla media
    elif nuovi_casi > media_nuovi_casi * 1.5:
        casi_moltiplicatore = 1.1  # Alti rispetto alla media
    elif nuovi_casi >= media_nuovi_casi * 0.8:
        casi_moltiplicatore = 1.0  # Vicini alla media
    elif nuovi_casi >= media_nuovi_casi * 0.5:
        casi_moltiplicatore = 0.8  # Moderatamente bassi
    elif nuovi_casi >= media_nuovi_casi * 0.3:
        casi_moltiplicatore = 0.7  # Bassi rispetto alla media
    else:
        casi_moltiplicatore = 0.5  # Molto bassi rispetto alla media

    #5) Moltiplicatore in base al rapporto positivi/tamponi
    rapporto_positivi = tamponi_positivi_settimanali / tamponi_settimanali

    if rapporto_positivi < media_rapporto_positivi * 0.3:
        tamponi_moltiplicatore = 0.7  # Molto inferiore alla media
    elif rapporto_positivi < media_rapporto_positivi * 0.6:
        tamponi_moltiplicatore = 0.8  # Moderatamente inferiore alla media
    elif rapporto_positivi < media_rapporto_positivi * 0.9:
        tamponi_moltiplicatore = 0.9  # Leggermente inferiore alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.1:
        tamponi_moltiplicatore = 1.0  # Vicino alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.3:
        tamponi_moltiplicatore = 1.1  # Leggermente superiore alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.6:
        tamponi_moltiplicatore = 1.2  # Moderatamente superiore alla media
    else:
        tamponi_moltiplicatore = 1.3  # Molto superiore alla media


    #Calcolo della probabilità finale = prodotto dei moltiplicatori
    probabilita = (sintomi_moltiplicatore * durata_moltiplicatore * gravita_moltiplicatore * contatto_moltiplicatore * casi_moltiplicatore * tamponi_moltiplicatore * 100)

    dict_moltiplicatori = {
    "sintomi_moltiplicatore": sintomi_moltiplicatore,
    "durata_moltiplicatore": durata_moltiplicatore,
    "gravita_moltiplicatore": gravita_moltiplicatore,
    "contatto_moltiplicatore": contatto_moltiplicatore,
    "casi_moltiplicatore": casi_moltiplicatore,
    "tamponi_moltiplicatore": tamponi_moltiplicatore
    }

    #standardizzo per avere la probabilità massima, definita in modo che
    #se tutti i moltiplicatori sono massimi, non ho comunque il 100% di chance che sia covid

    moltiplicatori_max = 14.0  #leggermente piu alto del vero, in modo che 100% non esca mai
    moltiplicatori_min = 0.014
    prob_perc_standardizzata = ((probabilita - moltiplicatori_min) / (moltiplicatori_max - moltiplicatori_min)) 


    if prob_perc_standardizzata > 40:
        probabilita_finale = "Very high"
    elif prob_perc_standardizzata > 25:
        probabilita_finale = "high"
    elif prob_perc_standardizzata > 15:
        probabilita_finale = "Medium"
    elif prob_perc_standardizzata> 5:
        probabilita_finale = "Low"
    else:
        probabilita_finale = "Very low"

    return probabilita_finale, dict_moltiplicatori, round(prob_perc_standardizzata, 1)


