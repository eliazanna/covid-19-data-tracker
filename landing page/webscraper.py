import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Importa By
from time import sleep
import pyperclip
import pandas as pd
from io import StringIO

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Configurazione delle opzioni di Chrome
options = webdriver.ChromeOptions() ;
prefs = {"download.default_directory" : r"C:\Users\eliza\Documents\GitHub\covid-19-data-tracker\csv usati\\"}; #perso le ore perche sensa rstring il path non veniva rispettato
options.add_experimental_option("prefs",prefs);


# Percorso al ChromeDriver
driver_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/chromedriver.exe"
service = Service(driver_path)

# Inizializzazione del driver
driver = webdriver.Chrome(service=service, options=options)



# URL da aprire
url = 'https://github.com/pcm-dpc/COVID-19/commits'
while True:
    try:           
        #importo i dati settimanali dell'Italia
        driver.get(url)
        sleep(2) 
        driver.find_element(By.PARTIAL_LINK_TEXT, "Pubblicazione del").click()
        sleep(2) 
        driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/main/turbo-frame/div/div/diff-layout/div[2]/div[2]/div[1]/div[2]/copilot-diff-entry[8]/div/div[1]/div[2]/div/details/summary").click()
        sleep(0.3)
        driver.find_element(By.PARTIAL_LINK_TEXT, "View file").click()
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Copy raw content"]').click()
        sleep(1)
        dati_copiati_italia = pyperclip.paste()

        #I start to manage the list, to confront the data from the scraper, with the one in the df
        lista_dati = dati_copiati_italia.split(",")
        new_datastr= lista_dati[23]
        new_data= new_datastr[32:42]
        df=pd.read_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_italy.csv")
        ultima_data_salvata = df.iloc[0, 0]
        print(ultima_data_salvata)
        print(new_data)

        #ITALIANS datas, scraping from the list imported 
        totale_positivi = int(lista_dati[29]) 
        terapie_intensive = int(lista_dati[26])
        morti_totali= int(lista_dati[33])
        tot_ospedalizzati= int(lista_dati[27])
        tot_casi= int(lista_dati[36])

        if ultima_data_salvata == new_data:
            print('nothing to change')
        else:

            dati_settimana = {"data":  [new_data],"totali positivi": [totale_positivi], "casi totali": [tot_casi],  "terapie intensive": [terapie_intensive],"morti totali": [morti_totali],"tot ospedalizzati": [tot_ospedalizzati]}
            df_nuova_riga = pd.DataFrame(dati_settimana)
            df = pd.concat([ df_nuova_riga, df])
            df.to_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_italy.csv", index=False)  
            print('Dati nuova sett. aggiunti')


            #importo i dati settimanali sulle regioni, solo se la data, nuova, non è gia presente nel df
            file_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/dpc-covid19-ita-regioni.csv"
            os.remove(file_path) #elimino il vecchio csv sulle regioni, in modo da poter scaricare quello nuovo
            driver.back()
            sleep(2)
            driver.find_element(By. XPATH, "/html/body/div[1]/div[4]/div/main/turbo-frame/div/div/diff-layout/div[2]/div[2]/div[1]/div[3]/div/copilot-diff-entry[12]/div/div[1]/div[2]/div/details").click()
            sleep(2)
            driver.find_element(By.PARTIAL_LINK_TEXT, "View file").click()
            sleep(2)
            driver.find_element(By.CSS_SELECTOR, 'button[data-testid="download-raw-button"]').click()
            sleep(3)



            #REGION datas, operation done only if new date:
            #the df has been saved as "dpc-covid19-ita-regioni.csv"
            df = pd.read_csv(file_path)

            df['data'] = pd.to_datetime(df['data']).dt.date  # tengo solo la data, senza ora
            start_date = "2024-01-04"
            df = df[df['data'] >= pd.to_datetime(start_date).date()]

            columns_to_keep = ['data', 'denominazione_regione', 'totale_positivi', 'nuovi_positivi', 'totale_positivi_test_antigenico_rapido', 'tamponi_test_antigenico_rapido']
            df = df[columns_to_keep]

            #passaggio logico particolare, raggruppo le settimane e ne creo una colonna per poter poi "gruoppare" per essa (poi toglierò la colonna) 
            df['custom_week'] = ((pd.to_datetime(df['data']) - pd.to_datetime(start_date)).dt.days // 7)

            # Sostituisco i nomi di "P.A. Bolzano" e "P.A. Trento" con "Trentino-Alto Adige" nel DataFrame prima del raggruppamento
            df['denominazione_regione'] = df['denominazione_regione'].replace(['P.A. Bolzano', 'P.A. Trento'], 'Trentino-Alto Adige')
            df['denominazione_regione'] = df['denominazione_regione'].replace("Friuli Venezia Giulia", "Friuli-Venezia Giulia")
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
            weekly_df.to_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate_regions.csv", index=False)
            print("raggruppamento riuscito")

        break  
    except Exception:
        print('errore trovato')