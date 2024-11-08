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
        sintomi_moltiplicatore = 1.1
    else:
        sintomi_moltiplicatore = 1.2

    # 2) Moltiplicatore in base alla durata dei sintomi
    if durata_sintomi < 3:
        durata_moltiplicatore = 0.7  # Sintomi di breve durata, meno probabile COVID
    elif durata_sintomi <= 7:
        durata_moltiplicatore = 1.5  # Sintomi di durata moderata, probabilità standard
    else:
        durata_moltiplicatore = 2  # Sintomi di lunga durata, più probabile COVID

    # 3) Moltiplicatore in base alla gravità dei sintomi
    if gravita_sintomi == "lieve":
        gravita_moltiplicatore = 0.7  # Sintomi lievi, meno probabile COVID
    elif gravita_sintomi == "moderata":
        gravita_moltiplicatore = 1.0  # Sintomi moderati, probabilità standard
    else:
        gravita_moltiplicatore = 1.2  # Sintomi severi, più probabile COVID

    # 4. Moltiplicatore in base ai contatti con positivi confermati
    if contatto_con_positivi:
        contatto_moltiplicatore = 1.5 
    else:
        contatto_moltiplicatore=1

    if nuovi_casi > media_nuovi_casi * 3.0:
        casi_moltiplicatore = 1.8  # Molto più alti della media
    elif nuovi_casi > media_nuovi_casi * 2.0:
        casi_moltiplicatore = 1.5  # Molto alti rispetto alla media
    elif nuovi_casi > media_nuovi_casi * 1.5:
        casi_moltiplicatore = 1.3  # Alti rispetto alla media
    elif nuovi_casi > media_nuovi_casi * 1.2:
        casi_moltiplicatore = 1.1  # Moderatamente alti
    elif nuovi_casi >= media_nuovi_casi * 0.8:
        casi_moltiplicatore = 1.0  # Vicini alla media
    elif nuovi_casi >= media_nuovi_casi * 0.5:
        casi_moltiplicatore = 0.7  # Moderatamente bassi
    elif nuovi_casi >= media_nuovi_casi * 0.3:
        casi_moltiplicatore = 0.6  # Bassi rispetto alla media
    else:
        casi_moltiplicatore = 0.4  # Molto bassi rispetto alla media

    #5) Moltiplicatore in base al rapporto positivi/tamponi
    rapporto_positivi = tamponi_positivi_settimanali / tamponi_settimanali

    if rapporto_positivi < media_rapporto_positivi * 0.3:
        tamponi_moltiplicatore = 0.5  # Molto inferiore alla media
    elif rapporto_positivi < media_rapporto_positivi * 0.6:
        tamponi_moltiplicatore = 0.6  # Moderatamente inferiore alla media
    elif rapporto_positivi < media_rapporto_positivi * 0.9:
        tamponi_moltiplicatore = 0.8  # Leggermente inferiore alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.1:
        tamponi_moltiplicatore = 1.0  # Vicino alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.3:
        tamponi_moltiplicatore = 1.2  # Leggermente superiore alla media
    elif rapporto_positivi <= media_rapporto_positivi * 1.6:
        tamponi_moltiplicatore = 1.3  # Moderatamente superiore alla media
    else:
        tamponi_moltiplicatore = 1.5  # Molto superiore alla media


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

    #determino categoria di probabilità
    #valori attualmente un po random, sono fa fixare
    #sarebbe carino standardizzare i valori per avere un numero in percentuale
    if probabilita > 500:
        probabilita_finale = "Molto Alta"
    elif probabilita > 300:
        probabilita_finale = "Alta"
    elif probabilita > 200:
        probabilita_finale = "Media"
    elif probabilita > 100:
        probabilita_finale = "Bassa"
    else:
        probabilita_finale = "Molto Bassa"
    
    return probabilita_finale, dict_moltiplicatori
