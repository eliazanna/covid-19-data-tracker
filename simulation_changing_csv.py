import pandas as pd


# Simulo aggiunta nuova riga per il DataFrame weeklyupdate_italy
''' 
csv_path_italy= "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_italy.csv"
weeklyupdate_italy = pd.read_csv(csv_path_italy)
newline_italy = pd.DataFrame({ 
    'data': [pd.to_datetime("2024-11-13").date()],  # Conversione a datetime
    'totali positivi': [216335],
    'casi totali': [26905329],
    'terapie intensive': [73],
    'morti totali': [197714],
    'tot ospedalizzati': [2140]
})
weeklyupdate_italy=  pd.concat([newline_italy, weeklyupdate_italy], ignore_index=True)
weeklyupdate_italy.to_csv(csv_path_italy, index=False ) 
'''

#simulo rimozione riga weeklyupdate_italy
'''
csv_path_italy= "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_italy.csv"
weeklyupdate_italy = pd.read_csv(csv_path_italy)
weeklyupdate_italy = weeklyupdate_italy.drop(weeklyupdate_italy.index[0])
weeklyupdate_italy.to_csv(csv_path_italy, index=False)
'''

#simulo una rimozione 20 RIGHE in df weeklyupdate_regions
'''
csv_path_regions= "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"
weeklyupdate_regions = pd.read_csv(csv_path_regions)
weeklyupdate_regions= weeklyupdate_regions.drop(weeklyupdate_regions.index[0:20])
weeklyupdate_regions.to_csv(csv_path_regions, index=False)
'''