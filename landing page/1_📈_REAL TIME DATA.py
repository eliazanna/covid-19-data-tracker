import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from plots_functions import grafico_regioni
from plots_functions import plot_europe_map
from plots_functions import grafico_deaths_cases_italia


st.sidebar.success("Select a demo above.")

#CSS per modificare il background della pagina
st.markdown("""<style>.stApp { background-color: #f0f8ff;  } /*colore di sfondo della pagina */</style>""", unsafe_allow_html=True)


#file CSV con i dati settimanali
path_italia= "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_italy.csv"
path_regioni= "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"

df_italia = pd.read_csv(path_italia, nrows=3)
#prendo i dati più recenti (prima riga) e quelli della settimana precedente (seconda riga)
most_recent_data = df_italia.iloc[0]
previous_week_data = df_italia.iloc[1]
two_weeks_old_data= df_italia.iloc[2]

# Estrai i dati necessari dalle due righe
# Dati più recenti
now_positive = most_recent_data['totali positivi']
intensive_care = most_recent_data['terapie intensive']
hospital_patients = most_recent_data['tot ospedalizzati']
weekly_deaths = most_recent_data['morti totali'] - previous_week_data["morti totali"]
weekly_new_cases  = most_recent_data['casi totali'] - previous_week_data['casi totali']

# Dati della settimana precedente
prev_now_positive = previous_week_data['totali positivi']
prev_intensive_care = previous_week_data['terapie intensive']
prev_hospital_patients = previous_week_data['tot ospedalizzati']
prev_weekly_deaths = previous_week_data["morti totali"] - two_weeks_old_data["morti totali"]
prev_weekly_new_cases= previous_week_data['casi totali'] - two_weeks_old_data['casi totali']

# Calcolo delle variazioni percentuali per totali positivi, terapie intensive e ospedalizzati
change_now_positive = ((now_positive - prev_now_positive) / prev_now_positive) * 100
change_intensive_care = ((intensive_care - prev_intensive_care) / prev_intensive_care) * 100
change_hospital_patients = ((hospital_patients - prev_hospital_patients) / prev_hospital_patients) * 100
change_weekly_deaths = ((weekly_deaths - prev_weekly_deaths)/ prev_weekly_deaths) * 100
change_weekly_new_cases= ((weekly_new_cases - prev_weekly_new_cases)/prev_weekly_new_cases) * 100

#inizio interfaccia grafica

st.title("Real-Time COVID-19")
st.markdown('<h3 style="color:red;">Current situation compared to the previous week', unsafe_allow_html=True)      

lastdata= most_recent_data['data']
st.markdown(f"""<div style="text-align: right; color: #a9a9a9">Last update: {lastdata}</div>""",unsafe_allow_html=True)
st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 30px; margin-top: -5px; width: 100%;" />""", unsafe_allow_html=True )


#----------------------------------------------------------------------
#defining colors(1) and grafic boxes (2, with css)

#(1) freccia e valore percenutali colorati in base a delta
def format_delta(delta, value=None):
    arrow = "↑" if delta > 0 else "↓"
    color = "red" if delta > 0 else "green"

    if value is not None:
        return '<span style="color: ' + color + ';">' + str(value) + '</span>'
    else:
        return '<span style="color: ' + color + ';">' + arrow + ' ' + str(round(abs(delta), 1)) + '%</span>'

#2 creating boxes
st.markdown(
    """<style>.metric-box {
        border: 1px solid #d3d3d3; 
        padding: 2px;
        margin-bottom: 6px;  /* Spazio tra i box */
        border-radius: 10px;  /* Arrotonda i bordi */
        text-align: center;  /* Centra il testo */
    }
    .metric-label {font-size: 16px; color: #000000;}
    .metric-value {font-size: 28px;}
    .metric-delta {font-size: 14px;}</style>""",
    unsafe_allow_html=True
)


#-------------------------------------------------------------------
#creo due colonne ed inizio a riempirle, 
#quella a sinistra con i nuovi valori importati, colorati tramite la funzione 
#sovrastante e inseriti nei box. Quella a destra con mappa importata


col1, col2 = st.columns([1.5,1.3]) 
with col1: 
    st.write('')
    st.write('')
    st.markdown(f"""

    <div class="metric-box">
        <div class="metric-label">New Positives</div>
        <div class="metric-value">{format_delta(change_weekly_new_cases, value=int(weekly_new_cases))}</div>
        <div class="metric-delta">{format_delta(change_weekly_new_cases)}</div>
    </div>       
    <div class="metric-box">
        <div class="metric-label">Currently Positives</div>
        <div class="metric-value">{format_delta(change_now_positive, value=int(now_positive))}</div>
        <div class="metric-delta">{format_delta(change_now_positive)}</div>
    </div> 
    <div class="metric-box">
        <div class="metric-label">Currently in Intensive Care</div>
        <div class="metric-value">{format_delta(change_intensive_care, value=int(intensive_care))}</div>
        <div class="metric-delta">{format_delta(change_intensive_care)}</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Currently in Hospital</div>
        <div class="metric-value">{format_delta(change_hospital_patients, value=int(hospital_patients))}</div>
        <div class="metric-delta">{format_delta(change_hospital_patients)}</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">This week Deaths</div>
        <div class="metric-value">{format_delta(change_weekly_deaths, value=int(weekly_deaths))}</div>
        <div class="metric-delta">{format_delta(change_weekly_deaths)}</div>
    </div>
""", unsafe_allow_html=True)


#visualizziamo il grafico nella colonna di destra
with col2:
    

    fig1 = grafico_regioni('nuovi_positivi')
    fig2 = grafico_regioni('totale_positivi')
    scegli_grafico_regioni = st.selectbox("", ['Distribution of new cases (log scale)', 'Distribution of currently positive (log scale) '])


    # Mostra il grafico in base alla selezione
    df_regioni = pd.read_csv(path_regioni, nrows=20)  
   
    if scegli_grafico_regioni == 'Distribution of new cases (log scale)':
        grafico_da_mostrare = fig1
  
        regione_max_casi = df_regioni.loc[df_regioni['nuovi_positivi'].idxmax(), 'denominazione_regione']
        regione_min_casi = df_regioni.loc[df_regioni['nuovi_positivi'].idxmin(), 'denominazione_regione']
        numero_max = df_regioni['nuovi_positivi'].max()
        numero_min = df_regioni['nuovi_positivi'].min()
        st.pyplot(grafico_da_mostrare)
        st.markdown("Most new-cases: "  + "**" + str(regione_max_casi) + "**" + " (" + str(numero_max) + ")  \n"
         "Less new-cases: "  + "**" + str(regione_min_casi) + "**" + " (" + str(numero_min) + ")")

        
    else:
        grafico_da_mostrare = fig2
        regione_max_casi = df_regioni.loc[df_regioni['totale_positivi'].idxmax(), 'denominazione_regione']
        regione_min_casi = df_regioni.loc[df_regioni['totale_positivi'].idxmin(), 'denominazione_regione']
        numero_max = df_regioni['totale_positivi'].max()
        numero_min = df_regioni['totale_positivi'].min()
        st.pyplot(grafico_da_mostrare)
        st.markdown("Most total-positives: " + "**" + str(regione_max_casi) + "**" + " (" + str(numero_max) + ")  \n"
                    "Less total-positives: " + "**" + str(regione_min_casi) + "**" + " (" + str(numero_min) + ")")
    


st.markdown(
    """
    <style>
    .css-1lcbmhc, .css-1lcbmhc 
    { margin-bottom: -100px}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 15px; width: 100%;" />""", unsafe_allow_html=True )


# Breve spiegazione in base alla variazione percentuale dei casi totali
if change_weekly_new_cases > 10:
    st.write("a")

elif 0 < change_weekly_new_cases <= 10:
    st.write("b")

elif -10 < change_weekly_new_cases <= 0:
    st.write("c")

else:
    st.write("d")


# Sezione 2: Mappe e analisi dei dati storici
st.header("The effects of Covid-19 in Europe")

# Crea una tabella interattiva per scegliere i grafici
option = st.selectbox('',
    ('Total Cases per Million', 'Total Deaths per Million', 'Hospital Patients per Million'))
# Mostra il grafico in base alla selezione

if option == 'Total Cases per Million':
    st.write("**Total Cases per Million in Europe**")
    st.write("This map shows the total cases per million people in Europe, highlighting the spread of the virus across the continent.")
    fig3 = plot_europe_map(colonna='total_cases_per_million', cmap='OrRd', color_null=False) 
    st.pyplot(fig3)

elif option == 'Total Deaths per Million':
    st.write("**Total Deaths per Million in Europe**")
    st.write("This map displays the total deaths per million people in Europe, providing insight into the mortality impact.")
    fig4 = plot_europe_map(colonna='total_deaths_per_million', cmap='Greys', color_null=False)
    st.pyplot(fig4)

else:
    st.write("**Hospital Patients per Million in Europe**")
    st.write("This map shows the number of hospital patients per million people in Europe, reflecting the pressure on the healthcare system.")
    fig5 = plot_europe_map(colonna='hosp_patients_per_million', cmap='Blues', color_null=True)
    st.pyplot(fig5)

st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 15px; width: 100%;" />""", unsafe_allow_html=True )
#-------------------------------------------------------------------------------------

# Creazione di opzioni di selezione per il confronto
confronto = st.selectbox( "",
    ['Compare with vaccinated population', 'Compare with European average'])

# Mostra il grafico in base alla selezione
if confronto == 'Compare with vaccinated population':
    st.write("Comparing new deaths on new cases with the vaccinated population gives insight into the effectiveness of vaccination in reducing deaths.")
    st.pyplot(grafico_deaths_cases_italia(with_asintoti=True))

else:
    st.write("Comparing new deaths on new cases with the European average highlights how the country fares in relation to its neighbors.")
    st.pyplot(grafico_deaths_cases_italia(add_europa=True, with_asintoti=False))


st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 15px; width: 100%;" />""", unsafe_allow_html=True )
#--------------------------------------------------------------------------------------
#newsletter



@st.dialog("Iscrive here")
def subscribe():
    st.write("Get updates directly in your inbox. Please enter your details:")
    name = st.text_input("Your Name:")
    email = st.text_input("Email Address:")
    if st.button("Subscribe"):
        if name and email:
            st.session_state.subscription = {"name": name, "email": email}


            #metto nel csv
            path="C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/newsletter_list.csv"
            df_newsletter = pd.read_csv(path)
            newrow= pd.DataFrame({"name": [name] , "email": [email]})
            df_newsletter=pd.concat([newrow, df_newsletter])
            df_newsletter.to_csv((path), index=False)  #Salva il CSV aggiornato
            print("dati aggiunti")

            st.success(f"Thank you, {name}, for subscribing!")
        
        else:
            st.error("Please enter both your name and email.")

if "subscription" not in st.session_state:
    st.write("Join our newsletter for the latest updates!")
    if st.button("Subscribe", key="open_subscribe_dialog"):
        subscribe()
else:
    st.write(f"You are subscribed with the name: {st.session_state.subscription['name']} and email: {st.session_state.subscription['email']}")






