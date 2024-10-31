from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Importa By
from time import sleep
import pyperclip
import pandas as pd

#percorso al chromedriver
driver_path = "C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/chromedriver.exe"
options = webdriver.ChromeOptions()
# Inizializzazione del driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

url = 'https://github.com/pcm-dpc/COVID-19/commits' 


        
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


#importo i dati settimanali sulle regioni
driver.back()
sleep(2)
driver.find_element(By. XPATH, "/html/body/div[1]/div[4]/div/main/turbo-frame/div/div/diff-layout/div[2]/div[2]/div[1]/div[3]/div/copilot-diff-entry[11]/div/div[1]/div[2]/div/details/summary").click()
sleep(2)
driver.find_element(By.PARTIAL_LINK_TEXT, "View file").click()
sleep(1)
driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Copy raw content"]').click()
sleep(1)
dati_copiati_regioni = pyperclip.paste()


lista_dati = dati_copiati_italia.split(",")
new_datastr= lista_dati[23]
new_data= new_datastr[32:42]
totale_positivi = int(lista_dati[29]) 
terapie_intensive = int(lista_dati[26])
morti_totali= int(lista_dati[33])
tot_ospedalizzati= int(lista_dati[27])
tot_casi= int(lista_dati[36])

df=pd.read_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate.csv")
ultima_data_salvata = df.iloc[0, 1]
print(ultima_data_salvata)

if ultima_data_salvata == new_data:
    print('nothing to change')
#else:
    dati_settimana = {"data":  [new_data],"totali positivi": [totale_positivi], "casi totali": [tot_casi],  "terapie intensive": [terapie_intensive],"morti totali": [morti_totali],"tot ospedalizzati": [tot_ospedalizzati]}
    df_nuova_riga = pd.DataFrame(dati_settimana)
    df = pd.concat([ df_nuova_riga, df])
    df.to_csv("C:/Users/eliza/Documents/GitHub/covid-19-data-tracker/csv usati/weeklyupdate.csv", index=False)  
    print('Dati nuova sett. aggiunti')