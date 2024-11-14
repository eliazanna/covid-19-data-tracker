import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

def grafico_regioni(title, colonna):
    
    file_csv = "c:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv"
    shapefile_path = "c:/Users/eliza/Documents/GitHub/covid-19-data-tracker/geometrie/mappa italia/Reg01012024_g_WGS84.shp"

    df_csv = pd.read_csv(file_csv, nrows=20)
    data_piu_recente = df_csv['data'].max()
    df_csv = df_csv[df_csv['data'] == data_piu_recente] #tengo solo i dati piu recenti 

    df_shapefile = gpd.read_file(shapefile_path) #df su shapefile

    df_unito = df_shapefile.merge(df_csv, left_on='DEN_REG', right_on='denominazione_regione') #innerjoin tra i due

    #dal df unito, prendo la colonna specificata (variabile della funzione)
    #e la rendo in scala logaritmica con numpy. log(1+x)
    df_unito[colonna] = np.log1p(df_unito[colonna]) 

    fig, asse = plt.subplots(1, 1, figsize=(9, 9), facecolor='none') #creo una figura ed un asse, in griglia 1x1

    valore_min = df_unito[colonna].min()
    valore_max = df_unito[colonna].max()
    norm = colors.Normalize(valore_min, valore_max)

    df_unito.plot(column=colonna, cmap='OrRd', linewidth=1, ax=asse, edgecolor='black', legend=False, norm=norm)

    #colorbar orizzontale con normalizzazione
    mappatore_colori = plt.cm.ScalarMappable(cmap='OrRd', norm=norm)
    mappatore_colori._A = []
    colorbar = plt.colorbar(mappatore_colori, ax=asse, orientation='horizontal', fraction=0.02, pad=-0.1)
    colorbar.set_label('Scala logaritmica')# Aggiungi un'etichetta alla colorbar

    # Rimuovo cornice e valori sugli assi
    asse.set_frame_on(False)
    asse.set_xticks([])
    asse.set_yticks([])

    plt.title(title, fontsize=15)

    return fig


#per la colonna nuovi positivi (nessun titolo)
fig1 = grafico_regioni('', 'nuovi_positivi') 
plt.show() 

#per la colonna totale positivi (no tit)
fig2 = grafico_regioni('', 'totale_positivi')  # Per totale positivi
plt.show()  # Visualizza il grafico per i totali positivi