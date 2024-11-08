#gestoione grande csv settimanale
#l'obiettivo è continuare ad aggiornarlo con il webscraping tramite innerjoin

import pandas as pd
file_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/alltime_regions.csv"
df = pd.read_csv(file_path)


df['data'] = pd.to_datetime(df['data']).dt.date  # tengo solo la data, senza ora
start_date = "2024-01-04"
df = df[df['data'] >= pd.to_datetime(start_date).date()]

#tengo solo le colonne necessarie
columns_to_keep = ['data', 'denominazione_regione', 'totale_positivi', 'nuovi_positivi', 
                   'totale_positivi_test_antigenico_rapido', 'tamponi_test_antigenico_rapido']
df = df[columns_to_keep]

#raggruppo in settimane a partire da gennaio 3
df['custom_week'] = ((pd.to_datetime(df['data']) - pd.to_datetime(start_date)).dt.days // 7)

# Sostituisco i nomi di "P.A. Bolzano" e "P.A. Trento" con "Trentino-Alto Adige" nel DataFrame prima del raggruppamento
df['denominazione_regione'] = df['denominazione_regione'].replace(['P.A. Bolzano', 'P.A. Trento'], 'Trentino-Alto Adige')

# Raggruppo i dati settimanalmente in base a 'denominazione_regione' e 'custom_week'
# necessito di grouppare tramite due colonne!!

weekly_df = df.groupby(['denominazione_regione', 'custom_week'], as_index=False).agg(
    data=('data', 'last'),  # Ultimo giorno della settimana
    nuovi_positivi=('nuovi_positivi', 'sum'),  # Somma dei nuovi positivi
    totale_positivi=('totale_positivi', 'last'),  # Ultimo valore della settimana
    totale_positivi_test_antigenico_rapido=('totale_positivi_test_antigenico_rapido', 'last'),
    tamponi_test_antigenico_rapido=('tamponi_test_antigenico_rapido', 'last')
)

# Calcolo dlele nuove colonne "tamponi_settimanali" e "tamponi_positivi_settimanali"
weekly_df['tamponi_settimanali'] = weekly_df.groupby('denominazione_regione')['tamponi_test_antigenico_rapido'].diff().fillna(0)
weekly_df['tamponi_positivi_settimanali'] = weekly_df.groupby('denominazione_regione')['totale_positivi_test_antigenico_rapido'].diff().fillna(0)

weekly_df = weekly_df.sort_values(by=['data', 'denominazione_regione'], ascending=[False, True])
weekly_df = weekly_df.drop(columns=['custom_week']) #rimuvo colonna inutile

#riordino e salvo
weekly_df = weekly_df[['data', 'denominazione_regione', 'nuovi_positivi', 'totale_positivi', 'tamponi_settimanali', 'tamponi_positivi_settimanali', 'tamponi_test_antigenico_rapido', 'totale_positivi_test_antigenico_rapido' ]]
weekly_df.to_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/alltime_regions_weekly.csv", index=False)

print("raggruppamento riuscito")
