# COVID GAME

import streamlit as st
import pandas as pd
from datetime import datetime
from covid_game_algorithm import calcola_probabilita  # Importa la funzione dal file dell'algoritmo

# Percorso del file CSV con i dati settimanali
file_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"
df = pd.read_csv(file_path)

df['data'] = pd.to_datetime(df['data']).dt.date #tengo solo la data

# Titolo e descrizione del progetto
st.title("Was it COVID?")
st.write("Un'interfaccia interattiva per stimare la probabilità che i tuoi sintomi fossero dovuti al COVID-19.")

# Punto 0: Checkbox per i sintomi attuali
attualmente_con_sintomi = st.checkbox("Attualmente ho i sintomi")

# Punto 1: Selezione dei sintomi
st.write("**Seleziona i sintomi che hai avuto (o che hai attualmente)**")
sintomi = ["Febbre", "Tosse", "Perdita dell'olfatto", "Mal di gola", "Stanchezza", "Altro"]
sintomi_selezionati = st.multiselect("Sintomi:", sintomi)

# Punto 2: Selezione della settimana dei sintomi (solo se non ha sintomi attualmente)
if attualmente_con_sintomi:
    settimana_scelta = df['data'].max()  # Seleziona automaticamente la data più recente
else:
    st.write("**Seleziona l'ultima settimana in cui hai avuto i sintomi**")
    fine_settimana = df['data'].unique()
    #inizio_settimana = fine_settimana - pd.Timedelta(days=6)
    
    settimana_scelta = st.selectbox("Settimana dei sintomi:", fine_settimana)

# Punto 3: Selezione della regione
st.write("**Seleziona la tua regione**")
regioni = df['denominazione_regione'].unique()
regione_scelta = st.selectbox("Regione:", regioni)

#4: Durata dei sintomi
st.write("**Durata dei sintomi (in giorni)**")
durata_sintomi = st.slider("Seleziona la durata dei sintomi in giorni:", min_value=1, max_value=30, value=5)

#5: Gravità dei sintomi
st.write("**Gravità dei sintomi**")
gravita_sintomi = st.selectbox("Seleziona la gravità dei sintomi:", ["Lieve", "Moderata", "Severa"])

#6: Contatti con positivi
st.write("**Contatti con positivi confermati**")
contatto_con_positivi = st.checkbox("Hai avuto contatti con una persona positiva al COVID-19")

# Bottone per calcolare la probabilità
if st.button("Calcola la probabilità"):
    # Calcola la probabilità usando l'algoritmo
    probabilita, dict_moltiplicatori, prob_perc_standardizzata = calcola_probabilita(
        df=df,
        regione=regione_scelta,
        settimana=settimana_scelta,
        sintomi=sintomi_selezionati,
        durata_sintomi=durata_sintomi,
        gravita_sintomi=gravita_sintomi,
        contatto_con_positivi=contatto_con_positivi
    )

    # Calcolo delle statistiche per la spiegazione
    df_RegSelez =  df[df['denominazione_regione'] == regione_scelta] #df in quella regione
    dati_selezionati = df_RegSelez[df_RegSelez['data'] == settimana_scelta] #df in quella data, in quella regione
    
    nuovi_casi = dati_selezionati['nuovi_positivi'].values[0]
    tamponi_settimanali = dati_selezionati['tamponi_settimanali'].values[0]
    tamponi_positivi_settimanali = dati_selezionati['tamponi_positivi_settimanali'].values[0]
    
    # Calcolo media storica
    media_nuovi_casi = df_RegSelez['nuovi_positivi'].mean()
    percentuale_diff = ((nuovi_casi - media_nuovi_casi) / media_nuovi_casi) * 100
    media_rapporto_positivi = (df_RegSelez['tamponi_positivi_settimanali'] /df_RegSelez['tamponi_settimanali']).mean() * 100
    rapporto_positivi = (tamponi_positivi_settimanali / tamponi_settimanali) * 100

    st.subheader("Risultati dell'analisi:")

    #messaggio relativo a sintomi attualmente
    if attualmente_con_sintomi:
        st.write("Hai selezionato che hai attualmente sintomi. Prenderemo dunque in considerazione la settimana più recente")
    
    #messaggio relativo ai sintomi selezionati
    if len(sintomi_selezionati) == 0:
        st.write("Non hai selezionato sintomi specifici, la probabilità che si tratti di un'infezione da Covid-19 è marginale")
    
    #Messaggio relativo alla durata dei sintomi
    if durata_sintomi < 3:
        st.write("I sintomi sono durati poco, il che può indicare una minore probabilità di contagio, facilmente si tratta di un semplice raffreddore.")
    elif durata_sintomi <= 7:
        st.write("I sintomi hanno avuto una durata moderata, non ci dice molto sulle possibilità di contagio, saranno utili i prossimi passaggi.")
    else:
        st.write("I sintomi sono durati molto, questo fattore suggerisce un aumento delle possiblità che si tratti di Covid-19 .")

    # Messaggio relativo alla gravità dei sintomi
    if gravita_sintomi == "Lieve":
        st.write("La gravità dei sintomi è lieve: la probabilità si abbassa")
    elif gravita_sintomi == "Moderata":
        st.write("La gravità dei sintomi è moderata: Questo dato suggerisce un possibile contagio, ma non ci dice molto")
    else:
        st.write("La gravità dei sintomi è elevata: Molto spesso il Covid si manifesta con sintomi più duri di una normale influenza, questo ci suggerisce un aumento delle probabilità di contagio")

    # Messaggio relativo ai contatti con positivi
    if contatto_con_positivi:
        st.write("Il fatto che tu abbia avuto contatti con un positivo fa riflettere... Ti serviva veramente un softwere per capire che eri ad alto rischio?")
    
    # Messaggio relativo alla differenza percentuale dei nuovi casi rispetto alla media
    if percentuale_diff > 0:
        st.write("Quella settimana, i nuovi contagi in " + regione_scelta + " sono stati il " + str(round(percentuale_diff, 1)) + "% in più rispetto alla media dei contagi di tutto l'anno, in tale regione.")
    else:
        st.write("Quella settimana, i nuovi contagi in " + regione_scelta + " sono stati il " + str(round(abs(percentuale_diff), 1)) + "% in meno rispetto alla media dei contagi di tutto l'anno, in tale regione.")

    # Messaggio 1 sui tamponi e rapporto di positività
    st.write("I tamponi effettuati sono stati " + str(int(tamponi_settimanali)) + ", con un tasso di positività del " + str(round(rapporto_positivi, 1)) + "%.")
    st.write("Mediamente, il valore percentuale di tamponi positivi in " + regione_scelta + " è " + str(round(media_rapporto_positivi, 1)) + "%.")

    # Messaggio 2 sui tamponi basato sul rapporto di positività
    if rapporto_positivi < media_rapporto_positivi * 0.5:
        st.write("Il rapporto di positività è molto inferiore alla media, suggerendo una possibilità alta che si trattasse di un'influenza e non COVID.")
    elif rapporto_positivi < media_rapporto_positivi:
        st.write("Il rapporto di positività è inferiore alla media, suggerendo una possibilità moderata che si trattasse di un'influenza, e non COVID.")
    elif rapporto_positivi <= media_rapporto_positivi * 1.1:
        st.write("Il rapporto di positività è vicino alla media, quindi la probabilità che fosse COVID è neutra.")
    elif rapporto_positivi <= media_rapporto_positivi * 1.5:
        st.write("Il rapporto di positività è superiore alla media, suggerendo una possibilità moderata che fosse COVID.")
    else:
        st.write("Il rapporto di positività è molto superiore alla media, suggerendo una possibilità alta che fosse COVID.")

    #risultato della probabilità finale
    st.subheader("Probabilità finale:")
    color = "green" if probabilita in ["Molto Bassa" ,"Bassa"] else "orange" if probabilita== "Media" else "red"
    testo = probabilita + ": " + str(round(prob_perc_standardizzata, 1)) + "%"
    html_testo = "<h2 style='color:" + color + ";'>" + testo + "</h2>" #colore e testo ma in stringa html
    st.markdown(html_testo, unsafe_allow_html=True)
    

    #DA TOGLIERE: Debug PER ME Mostra i valori dei MOLTIPLICATORI
    if dict_moltiplicatori:
        st.write("Valori dei dict_moltiplicatori (Debug)") 
        for key in dict_moltiplicatori: #dictionary
           st.write(key + ": " + str(dict_moltiplicatori[key]))
