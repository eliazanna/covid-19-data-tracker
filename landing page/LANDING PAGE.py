import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from plot_color_regions import grafico_regioni


# Aggiungere stile CSS per modificare il colore di tutto il testo e il background della pagina
st.markdown(
    
     """
    <style>
     /*colore di sfondo della pagina */
    .stApp { background-color: #f5f5f5;  }

    /* Colore di sfondo secondario*/
    .css-1d391kg, .css-1aumxhk {background-color: #fffceb; }

    /* testo principale */
    h1, h2, h3, h4, h5, h6, p, label {#4d4d4d; }

    .stMarkdown p {color: #4d4d4d;}
    .stRadio label {color: #4d4d4d}
    
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Real-Time COVID-19")


st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 50px; width: 100%;" />""", unsafe_allow_html=True )

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

# Creazione delle colonne
col1, col2 = st.columns([1.5,1.3]) 

#freccia e valore percenutali colorati in base a delta
def format_delta(delta, value=None):
    arrow = "↑" if delta > 0 else "↓"
    color = "red" if delta > 0 else "green"

    if value is not None:
        return '<span style="color: ' + color + ';">' + str(value) + '</span>'
    else:
        return '<span style="color: ' + color + ';">' + arrow + ' ' + str(round(abs(delta), 1)) + '%</span>'


# CSS per creare i box
st.markdown(
    """
    <style>
    .metric-box {
        border: 1px solid #d3d3d3; 
        padding: 2px;
        margin-bottom: 6px;  /* Spazio tra i box */
        border-radius: 10px;  /* Arrotonda i bordi */
        text-align: center;  /* Centra il testo */
    }
    .metric-label {font-size: 16px; color: #000000;}
    .metric-value {font-size: 28px;}
    .metric-delta {font-size: 14px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Mostra i dati con i box attorno
with col1: 
    st.markdown('<h2 style="color:red;">Current Situation. <br> Compared to the previous week</h2>', unsafe_allow_html=True)        
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
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    fig1 = grafico_regioni('', 'nuovi_positivi')
    fig2 = grafico_regioni('', 'totale_positivi')
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

