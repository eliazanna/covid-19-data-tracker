# COVID GAME

import streamlit as st
import pandas as pd
from covid_game_algorithm import calcola_probabilita  # Importa la funzione dal file dell'algoritmo

#per i colori non funziona il metodo theming consigliato da streamlit
#uso html

st.markdown(
    """
    <style>
     /*colore di sfondo della pagina */
    .stApp { background-color: #fff3b1;  }

    /* Colore di sfondo secondario*/
    .css-1d391kg, .css-1aumxhk {background-color: #fffceb; }

    /* testo nero */
    h1, h2, h3, h4, h5, h6, p, label {color: #000000; }
    </style>
    """,
    unsafe_allow_html=True
)


# Percorso del file CSV con i dati settimanali
file_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"
df = pd.read_csv(file_path)

df['data'] = pd.to_datetime(df['data']).dt.date #tengo solo la data

# Titolo e descrizione del progetto
st.title("Is it Covid-19?   Let's play!")
st.markdown("A non-scientific way to estimate the probability of being affected.  \n""This game is composed of 7 simple questions, good luck!")
st.markdown("""<hr style="border:0.1px solid gray; margin-top: 10px;">""", unsafe_allow_html=True) #linea

# Punto 0: Checkbox per i sintomi attuali
scelta_utente = st.radio("**1) How do you feel right now?**",  
["I feel good! Thank you", "Not very good"] )

if scelta_utente == "I feel good! Thank you":
    st.markdown("😊We are very happy to hear this!  \n""In this case the purpose is to analyze the last time you felt sick by comparing your symptoms with some data, to estimate the probability that you were affected by COVID-19. Let's get started!")
else:
    st.write("😞 Get well soon, warrior!")


# Punto 1: Selezione della settimana dei sintomi (solo se non ha sintomi attualmente)
if scelta_utente != "I feel good! Thank you":
    settimana_scelta = df['data'].max()  # Seleziona automaticamente la data più recente
else:
    fine_settimana = df['data'].unique()
    #inizio_settimana = fine_settimana - pd.Timedelta(days=6)
    settimana_scelta = st.selectbox("****2) Select the last week you had symptoms****", fine_settimana)


# Punto 2: Selezione dei sintomi
sintomi = ["Fever", "Cough", "Loss of smell", "Sore throat", "Fatigue", "Other"]
if scelta_utente != "I feel good! Thank you":
    sintomi_selezionati = st.multiselect("**2) Select the symptoms you are experiencing**", sintomi)
else:
    sintomi_selezionati = st.multiselect("**3) Select the symptoms you had**", sintomi)

# Punto 3: Selezione della regione
regioni = df['denominazione_regione'].unique()
if scelta_utente != "I feel good! Thank you":
    regione_scelta = st.selectbox("**3) Select your region**", regioni)
else:
    regione_scelta = st.selectbox("**4) Select your region**", regioni)

#4: Durata dei sintomi
if scelta_utente != "I feel good! Thank you":
    durata_sintomi = st.slider("**4) How many days have you had symptoms?**", min_value=1, max_value=30, value=5)
else:
    durata_sintomi = st.slider("**5) How many days did you have symptoms?**", min_value=1, max_value=30, value=5)

#5: Gravità dei sintomi
if scelta_utente != "I feel good! Thank you":
    gravita_sintomi = st.selectbox("**5) Select the severity of symptoms:**", ["Low", "Mid", "High"])
else:
    gravita_sintomi = st.selectbox("**6) Select the severity of symptoms:**", ["Low", "Mid", "High"])

#6: Contatti con positivi
if scelta_utente != "I feel good! Thank you":
    contatto_con_positivi = st.checkbox("**6) I have had contact with someone positive for COVID-19**")
else:
    contatto_con_positivi = st.checkbox("**7) I have had contact with someone positive for COVID-19**")

# Bottone per calcolare la probabilità
if st.button("Calculate probability"):
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

    st.markdown("""<hr style="border:0.1px solid gray; margin-top: 30px;">""", unsafe_allow_html=True) #linea
    
    st.subheader("Analysis results:")

    #messaggio relativo a sintomi attualmente
    if scelta_utente != "I feel good! Thank you":
        st.write("You indicated that you currently have symptoms. Therefore, we will consider the most recent week.")
    
    #messaggio relativo ai sintomi selezionati
    if len(sintomi_selezionati) == 0:
        st.write("You did not select any specific symptoms, so the probability of a COVID-19 infection is marginal.")
    
    #Messaggio relativo alla durata dei sintomi
    if durata_sintomi < 3:
        st.write("The symptoms lasted only a short time, which may indicate a lower probability of infection, possibly just a common cold.")
    elif durata_sintomi <= 7:
        st.write("The symptoms lasted for a moderate period, which doesn’t give much information about the likelihood of infection; the following points will help.")
    else:
        st.write("The symptoms lasted a long time, which suggests an increased chance that it could be COVID-19.")

    # Messaggio relativo alla gravità dei sintomi
    if gravita_sintomi == "Low":
        st.write("The severity of the symptoms is mild, which lowers the probability.")
    elif gravita_sintomi == "Mid":
        st.write("The severity of the symptoms is moderate. This suggests a possible infection but doesn't tell us much.")
    else:
        st.write("The severity of the symptoms is high. COVID-19 often presents with more intense symptoms than a common flu, suggesting an increased probability of infection.")

    # Messaggio relativo ai contatti con positivi
    if contatto_con_positivi:
        st.write("The fact that you had contact with someone positive for COVID-19 is concerning... Did you really need software to realize you were at high risk?")
    
    # Messaggio relativo alla differenza percentuale dei nuovi casi rispetto alla media
    if percentuale_diff > 0:
        st.write("That week, new cases in " + regione_scelta + " were " + str(round(percentuale_diff, 1)) + "% higher than the average cases throughout the year in that region.")
    else:
        st.write("That week, new cases in " + regione_scelta + " were " + str(round(abs(percentuale_diff), 1)) + "% lower than the average cases throughout the year in that region.")

    # Messaggio 1 sui tamponi e rapporto di positività
    st.write("The tests conducted were " + str(int(tamponi_settimanali)) + ", with a positivity rate of " + str(round(rapporto_positivi, 1)) + "%.")
    st.write("On average, the percentage of positive tests in " + regione_scelta + " is " + str(round(media_rapporto_positivi, 1)) + "%.")


    # Messaggio 2 sui tamponi basato sul rapporto di positività
    if rapporto_positivi < media_rapporto_positivi * 0.5:
        st.write("The positivity rate is much lower than average, suggesting a high chance that it was a flu, not COVID.")
    elif rapporto_positivi < media_rapporto_positivi:
        st.write("The positivity rate is below average, suggesting a moderate chance that it was a flu, not COVID.")
    elif rapporto_positivi <= media_rapporto_positivi * 1.1:
        st.write("The positivity rate is close to average, so the probability it was COVID is neutral.")
    elif rapporto_positivi <= media_rapporto_positivi * 1.5:
        st.write("The positivity rate is above average, suggesting a moderate chance it was COVID.")
    else:
        st.write("The positivity rate is much higher than average, suggesting a high chance it was COVID.")

    #risultato della probabilità finale
    st.subheader("Final Probability:")
    color = "green" if probabilita in ["Molto Bassa" ,"Bassa"] else "orange" if probabilita== "Media" else "red"
    testo = probabilita + ": " + str(round(prob_perc_standardizzata, 1)) + "%"
    html_testo = "<h2 style='color:" + color + ";'>" + testo + "</h2>" #colore e testo ma in stringa html
    st.markdown(html_testo, unsafe_allow_html=True)
    

    #DA TOGLIERE: Debug PER ME Mostra i valori dei MOLTIPLICATORI
    #if dict_moltiplicatori:
    #    st.write("Valori dei dict_moltiplicatori (Debug)") 
    #    for key in dict_moltiplicatori: #dictionary
     #      st.write(key + ": " + str(dict_moltiplicatori[key]))
