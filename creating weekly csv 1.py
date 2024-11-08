import pandas as pd

#creo il csv sul path
file_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate.csv"


# inserisco i valori delle settimane precedenti

df = pd.DataFrame({ 
'data' : pd.to_datetime(["2024-10-23", "2024-10-16", "2024-10-09", "2024-10-02"]) , # Conversione a datetime
'totali positivi': [221875, 220071, 217233,216335],
'casi totali': [26936475, 26927813, 26916381, 26905329]  ,
'terapie intensive' : [76, 86, 71, 73],
'morti totali' : [198047, 197931, 197814, 197714],
'tot ospedalizzati' : [2350, 2441, 2220, 2140]
})

#salvo il csv sul percorso
df.to_csv(file_path, index=False )

