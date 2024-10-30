from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Importa By
from time import sleep
import pyperclip

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
print(dati_copiati_italia)

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
print(dati_copiati_regioni)

#capire come importarli su dataframe e dove salvarlo

#capire come confrontarli con dati settimana prima

#capire come fare controllo su dataframe, se dati sono uguali non modificare

