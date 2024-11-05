import pandas as pd
import geopandas as gpd


doc = pd.read_csv('C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/covid-data.csv')

#prendo i paesi europei, con date a partire da 16 febbraio
#elimino i dati di scozia inghilterra, wales e Northern ireland, perche gia rappresentati in UK
europa = doc[(doc['continent'] == 'Europe') & (doc['date'] > '2020-02-10')]
europa = europa[~europa['location'].isin(['England', 'Northern Ireland', 'Wales', 'Scotland'])]

#tengo solo colonne che mi interessano
europa = europa[['date', 'location', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
        'hosp_patients', 'total_cases_per_million', 'new_cases_per_million',
        'total_deaths_per_million', 'new_deaths_per_million', 'hosp_patients_per_million']]

#elimino le righe con new_cases = '0'
filtered=europa[europa['new_cases']!=0]
print(filtered)


