import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

'''Firt, i clean the csv file, to filter the data i need for the plots, 
then i upload the "world" shapefile df: a dataframe that contains informations about geometric positions of the countries.
considering that late i have to innerjoin "world" with the csv of data informations on the countries, 
I also correct states with a different name (to align it with the one given in the other csv) '''

doc = pd.read_csv('C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/covid-data.csv')

#prendo i paesi europei, con date a partire da 10 febbraio
#elimino i dati di scozia inghilterra, wales e Northern ireland, perche gia rappresentati in UK
europa = doc[(doc['continent'] == 'Europe') & (doc['date'] > '2020-02-15')]
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

#----------------------------------------------------------------------------------------------------------------
'''Creates a choropleth map of Europe based on data from a selected column (variable).
The maximum value of the selected column is computed for each country,
and these values are assigned to the geometries of each country (via an inner join on "world").
If the third parameter is True, countries without data will be visually distinguished.'''

def plot_europe_map(colonna, cmap, color_null=True):
    
    #prendo il valore massimo di ogni paese, nella "colonna" (variabile), e lo metto in un dataframe
    dpm_country = filtered.groupby('location')[colonna].max().reset_index()
    dpm_country = dpm_country.rename(columns={'location': 'SOVEREIGNT'}) #per poter fare innerjoin

    europe_map = world.merge(dpm_country, on='SOVEREIGNT', how='inner') #innerjoin

    #divido i paesi con dati validi e quelli con dati nulli
    europe_map_valid = europe_map[europe_map[colonna] > 0]
    europe_map_null = europe_map[pd.isna(europe_map[colonna])]
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.set_facecolor('none') #rimuovo sfondo
    fig.patch.set_alpha(0)
    europe_map_valid.plot(column=colonna, cmap=cmap, linewidth=0.2, ax=ax, edgecolor='black', legend=True, aspect='equal')
    
    if color_null: #Condizione per colorare gli stati nulli (uso solo nel terzo grafico)
        europe_map_null.plot(ax=ax, color='none', edgecolor='#D3D3D3', hatch='//', linewidth=0.6, aspect='equal')
    
    ax.set_xlim([-10, 35])
    ax.set_ylim([35, 72])
    ax.set_xticks([]) #non voglio mostrare i valori 
    ax.set_yticks([])

    title_text = colonna.replace("_", " ") + " in Europe (COVID-19)"
    plt.title(title_text.upper(), fontsize=15)
    
    return fig

# Esempio di utilizzo (total cases)
#plot_europe_map(colonna='total_deaths_per_million', cmap='Greys', color_null=False)
#plt.show() 


#-------------------------------------------------------------------------------------------------------------
'''Creating the plots for another choreopletic map: this time about italy regions.
then, with numpy, i trasform the values of joined-df (column),  into a logaritmic scale values, to allow a better data visualisation.

Unlike the previous plot, I didn't like the default colorbar and decided to create a custom one below the plot. 
To achieve this, I had to normalize the colors based on the data in the CSV, as the default normalization ranges from 0 to 1.
'''

def grafico_regioni(colonna):

    
    file_csv = "c:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"
    italy_shapefile = gpd.read_file("c:/Users/eliza/Documents/GitHub/covid-19-data-tracker/geometrie/mappa italia/Reg01012024_g_WGS84.shp")

    df_csv = pd.read_csv(file_csv, nrows=20)
    data_piu_recente = df_csv['data'].max() 
    df_csv = df_csv[df_csv['data'] == data_piu_recente] #tengo solo i dati piu recenti 

    df_unito = italy_shapefile.merge(df_csv, left_on='DEN_REG', right_on='denominazione_regione') #innerjoin tra i due

    #dal df unito, prendo la colonna specificata (variabile della funzione)
    #e la rendo in scala logaritmica con numpy. log(1+x)
    df_unito[colonna] = np.log1p(df_unito[colonna]) 

    fig, asse = plt.subplots(1, 1, figsize=(9, 9), facecolor='none') #creo una figura ed un asse, in griglia 1x1
    df_unito.plot(column=colonna, cmap='OrRd', linewidth=1, ax=asse, edgecolor='black', legend=False)

    #colorbar orizzontale con normalizzazione
    valore_min = df_unito[colonna].min()
    valore_max = df_unito[colonna].max()
    norm = colors.Normalize(valore_min, valore_max) #normalize
    mappatore_colori = plt.cm.ScalarMappable(cmap='OrRd', norm=norm) #associating the color to the normalized values

    colorbar = plt.colorbar(mappatore_colori, ax=asse, orientation='horizontal', fraction=0.02, pad=-0.1)
    colorbar.set_label('Log scale')

    asse.set_frame_on(False) # Rimuovo cornice e valori sugli assi
    asse.set_xticks([])
    asse.set_yticks([])

    return fig


#per la colonna nuovi positivi
#grafico_regioni('nuovi_positivi') #/totale_positivi
#plt.show() 


#----------------------------------------------------------------------------------------------------------------------
'''Creates a line plot comparing the ratio of new deaths to new cases over time in Italy, with optional features:
1. By default, the graph shows monthly average ratios for Italy.
2. If `add_europa=True`, it adds the same ratio for Europe (excluding Italy) for comparison.
3. If `with_asintoti=True`, vertical dashed lines are added to indicate key vaccination milestones in Italy.
The X-axis is customized to show only the starting year for each period.
'''

def death_case_ratio(add_europa=False, with_asintoti=False):
    #dati per l'Italia
    italy_data = filtered[(filtered['location'] == 'Italy')].copy()
    italy_data['death_case_ratio'] = italy_data['new_deaths'] / italy_data['new_cases'] #create new column
    
    #Metto 'date' in formato datetime, e creo una colonna 'months' partendo da quella 'date'
    italy_data['date'] = pd.to_datetime(italy_data['date'])
    italy_data['month'] = italy_data['date'].dt.to_period('M')

    monthly_ratio = italy_data.groupby('month')['death_case_ratio'].mean().reset_index() #new df, include solo le due colonne in questione

    #grafico base per l'Italia
    fig, ax = plt.subplots(figsize=(12, 6))  # Creazione della figura e asse
    x_italy = monthly_ratio['month'].astype(str)
    y_italy = monthly_ratio['death_case_ratio']
    
    ax.plot(x_italy, y_italy, color='b', linewidth='1.2', label='Italy')
    ax.set_title('New deaths on new cases: Italy', fontsize=16, fontweight='bold', color='#333333')
    
    #Personalizzo le etichette dell'asse X per mostrare solo gli anni
    unique_years = monthly_ratio['month'].dt.year.unique()
    positions = [0, 12, 24, 36, 48] #positions of the year label
    ax.set_xticks(positions)
    ax.set_xticklabels(unique_years, fontsize=10, fontweight='bold')
    ax.tick_params(axis='y', labelsize=10)

    #asintoti vaccini, se richiesto
    if with_asintoti:
        ax.axvline(x='2021-05', color='gold', linestyle='--', linewidth=1, label='40% of the population vaccinated')
        ax.axvline(x='2021-07', color='#DAA520', linestyle='--',linewidth=1, label='50% of the population vaccinated')
        ax.axvline(x='2021-09', color='#FFB900', linestyle='--',linewidth=1, label='60% of the population vaccinated')

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
        ax.plot(x_europe, y_europe, color='r',linewidth=1 , label='Europe')
        ax.set_title('New deaths on new cases: Italy vs Europe', fontsize=16, fontweight='bold', color='#333333')
    
    ax.grid(visible=True, which='major', color='#E0E0E0', linestyle='-', linewidth=0.5)  # Griglia leggera
    ax.legend(loc='upper right', fontsize=10, frameon=False) 

    return fig


#grafico per l'Italia con il confronto Europa senza asintoti
#death_case_ratio(add_europa=True, with_asintoti=False)
#plt.show() 
