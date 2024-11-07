import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

doc = pd.read_csv('C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/covid-data.csv')

#prendo i paesi europei, con date a partire da 10 febbraio
#elimino i dati di scozia inghilterra, wales e Northern ireland, perche gia rappresentati in UK
europa = doc[(doc['continent'] == 'Europe') & (doc['date'] > '2020-02-10')]
europa = europa[~europa['location'].isin(['England', 'Northern Ireland', 'Wales', 'Scotland'])]

#tengo solo colonne che mi interessano
europa = europa[['date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
        'hosp_patients', 'total_cases_per_million', 'new_cases_per_million',
        'total_deaths_per_million', 'new_deaths_per_million', 'hosp_patients_per_million']]

#elimino le righe con new_cases = '0'
filtered=europa[europa['new_cases']!=0]


# carico il file che mi permette di fare il grafico sulla cartina 
shapefile_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/geometrie/mappa europa/ne_110m_admin_0_countries.shp"
world = gpd.read_file(shapefile_path)
world['SOVEREIGNT'] = world['SOVEREIGNT'].replace("Republic of Serbia", "Serbia") #different name didn't show Serbia before

#creo un dataframe/voc con le info per il primo grafico (stato, total_death_per_million)
dpm_country = filtered.groupby('location')['total_deaths_per_million'].max().reset_index()
dpm_country = dpm_country.rename(columns={'location': 'SOVEREIGNT'}) 

#innerjoin tra df con gli stati del csv (dpm_country), e quelli nella geometria (world), per tenere gli stati in comune
europe_map = world.merge(dpm_country, on='SOVEREIGNT', how='inner')

#tengo i paesi con valori non nulli
europe_map_valid = europe_map[europe_map['total_deaths_per_million'] > 0]

# Creo PLOT 1
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
europe_map_valid.plot(column='total_deaths_per_million', cmap='Greys', linewidth=0.2, ax=ax, edgecolor='black', legend=True, aspect='equal')

ax.set_xlim([-10, 35])  # Limiti di longitudine
ax.set_ylim([35, 72])   # Limiti di latitudine
plt.title('Total Deaths per Million in Europe (COVID-19)', fontsize=15)
#rimuovo i valori sugli assi x e y
ax.set_xticks([])
ax.set_yticks([])

plt.show()




#secondo grafico
tcpm_country = filtered.groupby('location')['total_cases_per_million'].max().reset_index()

tcpm_country = tcpm_country.rename(columns={'location': 'SOVEREIGNT'})
europe_map_cases = world.merge(tcpm_country, on='SOVEREIGNT', how='inner')

europe_map_cases_valid = europe_map_cases[europe_map_cases['total_cases_per_million'] > 0]

#CREO PLOT 2
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
europe_map_cases_valid.plot(column='total_cases_per_million', cmap='OrRd', linewidth=0.2, ax=ax, edgecolor='black', legend=True, aspect='equal')

ax.set_xlim([-10, 35])  # Limiti di longitudine
ax.set_ylim([35, 72])   # Limiti di latitudine
plt.title('Total Cases per Million in Europe (COVID-19)', fontsize=15)

#rimuovo i valori sugli assi x e y
ax.set_xticks([])
ax.set_yticks([])

plt.show()



#terzo grafico 
hp_country = filtered.groupby('location')['hosp_patients_per_million'].max().reset_index()
hp_country = hp_country.rename(columns={'location': 'SOVEREIGNT'})

europe_map_hospitals = world.merge(hp_country, on='SOVEREIGNT', how='inner')
europe_map_hospitals_valid = europe_map_hospitals[europe_map_hospitals['hosp_patients_per_million'] > 0]
europe_map_hospitals_null = europe_map_hospitals[pd.isna(europe_map_hospitals['hosp_patients_per_million'])]

#CREO PLOT 3
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
europe_map_hospitals_valid.plot(column='hosp_patients_per_million', cmap='Blues', linewidth=0.2, ax=ax, edgecolor='black', legend=True, aspect='equal')
europe_map_hospitals_null.plot(ax=ax, color='none', edgecolor='#D3D3D3', hatch='//', linewidth=0.6, aspect='equal')


ax.set_xlim([-10, 35])  # Limiti di longitudine
ax.set_ylim([35, 72])   # Limiti di latitudine
#rimuovo i valori sugli assi x e y
ax.set_xticks([])
ax.set_yticks([])

plt.title('Hospital Patients per Million in Europe (COVID-19)', fontsize=15)
plt.show()




# Funzione per grafici interenti alla pandemia in italia
def grafico_deaths_cases_italia(filtered, add_europa=False, with_asintoti=False):
    #dati per l'Italia
    italy_data = filtered[(filtered['location'] == 'Italy')].copy()
    italy_data['death_case_ratio'] = italy_data['new_deaths'] / italy_data['new_cases']
    

    #Metto 'date' in formato datetime, e creo una colonna 'months' partendo da quella 'date'
    italy_data['date'] = pd.to_datetime(italy_data['date'])
    italy_data['month'] = italy_data['date'].dt.to_period('M')
    monthly_ratio = italy_data.groupby('month')['death_case_ratio'].mean().reset_index()

    #grafico base per l'Italia
    x_italy = monthly_ratio['month'].astype(str)
    y_italy = monthly_ratio['death_case_ratio']
    
    plt.figure(figsize=(12,6))
    plt.plot(x_italy, y_italy, color='b', linewidth='1.2', label='Italy')
    plt.title('New deaths on new cases: Italy', fontsize=16, fontweight='bold', color='#333333' )
    
    #Personalizzo le etichette dell'asse X per mostrare solo gli anni
    unique_years = monthly_ratio['month'].dt.year.unique()
    positions = [monthly_ratio[monthly_ratio['month'].dt.year == year].index[0] for year in unique_years]
    plt.xticks(positions, unique_years, fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')

    #asintoti vaccini, se richiesto
    if with_asintoti:
        plt.axvline(x='2021-05', color='gold', linestyle='--', linewidth=1.5, label='40% of the population vaccinated')
        plt.axvline(x='2021-07', color='#DAA520', linestyle='--',linewidth=1.5, label='50% of the population vaccinated')
        plt.axvline(x='2021-09', color='#FFB900', linestyle='--',linewidth=1.5, label='60% of the population vaccinated')


    #confronto con Europa, se richiesto
    if add_europa:
        europe_data = filtered[filtered['location'] != 'Italy'].copy()
        europe_data['death_case_ratio'] = europe_data['new_deaths'] / europe_data['new_cases']
        europe_data['date'] = pd.to_datetime(europe_data['date'])
        europe_data['month'] = europe_data['date'].dt.to_period('M')
        europe_monthly = europe_data.groupby('month')['death_case_ratio'].mean().reset_index()

        x_europe = europe_monthly['month'].astype(str)
        y_europe = europe_monthly['death_case_ratio']

        # Aggiungo la linea dell'Europa al grafico
        plt.plot(x_europe, y_europe, color='r',linewidth=1 , label='Europe')
        plt.title('New deaths on new cases: Italy vs Europe', fontsize=16, fontweight='bold', color='#333333')
    
    plt.grid(visible=True, which='major', color='#E0E0E0', linestyle='-', linewidth=0.5)  # Griglia leggera
    plt.tight_layout()
    plt.legend(loc='upper right', fontsize=10, frameon=False) 
    plt.show()

#grafico solo per l'Italia senza asintoti
grafico_deaths_cases_italia(filtered, with_asintoti=False)

#grafico per l'Italia con gli asintoti
grafico_deaths_cases_italia(filtered, with_asintoti=True)

#grafico per l'Italia con il confronto Europa senza asintoti
grafico_deaths_cases_italia(filtered, add_europa=True, with_asintoti=False)

#grafico per l'Italia con il confronto Europa e con asintoti
grafico_deaths_cases_italia(filtered, add_europa=True, with_asintoti=True)