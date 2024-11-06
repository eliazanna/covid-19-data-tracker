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
# Rimuove i valori sugli assi x e y
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

# Rimuove i valori sugli assi x e y
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
# Rimuove i valori sugli assi x e y
ax.set_xticks([])
ax.set_yticks([])

plt.title('Hospital Patients per Million in Europe (COVID-19)', fontsize=15)
plt.show()