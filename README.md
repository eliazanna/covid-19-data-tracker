
## Table of Contents
1. [Introduction](#introduction)
2. [Page 1: Real Time Data](#page-1-real-time-data)
3. [Page 2: Covid Series](#page-2-covid-series)
4. [Page 3: Covid Game](#page-3-covid-game)
5. [Setup Instructions](#setup-instructions)
6. [Extras](#extras)


#Introduction
This project is designed to import, clean, and analyze Covid-19 data series. 
It features interactive visualizations and tools to explore both real-time and historical Covid-19 data.
Additionally, a "Covid Game" allows users to estimate the likelihood of infection based on symptoms and local trends.
The project is divided into 3 Streamlit pages:


1. #[page 1: Real Time Data](<landing page/1_📈_REAL TIME DATA.py>)- the principal page, in where:
    1) Are provided last weekly informations about the virus spread, to do that:
        a) I created the ["webscraper"](<landing page/webscraper.py>), a python file that allows me to automatize the importation of last Covid-19 information.
        The data are updated weekly by the "Italy Civil Protection Department", on this link: https://github.com/pcm-dpc/COVID-19.
        After this operation i will get [weeklyupdate_italy (1)](<csv usati/weeklyupdate_regions.csv>) and [weeklyupdate_regions (2)](<csv usati/weeklyupdate_italy.csv>).
        b) I manage the first (1), cleaning it and filtering the data I need to show.
    
    2) Creation of a choreopletic plot, that shows the spread of the virus in the italian regions on the last week. 
        a) To do that we need to innerjoin on the name of the regions: 
        the file (2), with the [italy geometric shapefile](<geometrie/mappa italia/Reg01012024_g_WGS84.shp>) to assign the informations I have into the geometric space covered by the regions.
        b) ALL the plots functions are written on ["plots_functions"](<landing page/plots_functions.py>), then called in the file i need them (in this case with: "from plots_functions import grafico_regioni").

    3) Creation of a newsletter subrscription box:
        a) To keep the code simple, I chose to implement only the functionality to save user names and email addresses to a [CSV file](<csv usati/newsletter_list.csv>).
        The system does not send emails automatically, but this could be achieved using libraries such as smtplib.



2. #[page 2: Covid Series](<landing page/pages/2_🌍_ COVID_SERIES.py>) : Page composed by [historic data](<csv usati/covid-data.csv>) of the Covid-19 pandemy, shows as plots* :
    
    1) A choropleth map of Europe (plot_europe_map):
        a) This map shows the spread of the virus across European countries based on the chosen data column (e.g., total cases, deaths per million, etc.).
        b) The map is created by joining the geometric shapefiles of the countries with the Covid-19 data. ([shapefile europa](<geometrie/mappa europa/ne_110m_admin_0_countries.shp>))
        c) Missing data for specific countries are visually represented using a distinct pattern or color, making it easier to identify gaps in the dataset.

    2)A line plot for Italy (grafico_deaths_cases_italia):
        a) This plot visualizes the ratio between new deaths and new cases for Italy, aggregated monthly.
        b) Optional features include:
           - Adding asymptotes to indicate vaccination milestones in Italy (e.g., 40%, 50%, and 60% of the population vaccinated).
           - Comparing Italy's data with the European average, visualized as a second line in the same graph.
        
    *as said before, the plots are all in the file["plots_functions"](<landing page/plots_functions.py>), then called in the main file by their function name.

    
3. #[page 3: Covid Game](<landing page/pages/3_🦠_COVID_GAME.py>)** This page introduces an interactive "Covid Game"** which provides a non-scientific estimation of the probability of being infected with Covid-19. It engages the user with a series of questions and calculates the likelihood of infection based on their responses and local data.

    1)User Interaction:
        The game consists of 7 questions divided into multiple steps:
        a) Current health status: The user can indicate whether they currently feel well or not. If they feel well, the analysis focuses on a previous time when they felt unwell.
        b) Symptom selection: Users can specify which symptoms they experienced and for how long.
        c) Region and week selection: The app uses the user's region and selected week to fetch local Covid-19 statistics.
        d) Contact history: Users can indicate whether they had contact with a confirmed positive case.

    2)Algorithm:
        The app uses a [calculation algorithm](<landing page/covid_game_algorithm.py>) implemented in a separate Python file.
        The algorithm considers user inputs (symptoms, duration, severity, contact history) and combines them with local Covid-19 trends (new cases, test positivity rates, historical averages).
        Each factor contributes a multiplier, resulting in a standardized probability score.
    
    3)Analysis Results:
        After answering the questions, the app provides:
        a) A detailed explanation of the probability calculation
        b) A final probability score (calculated by the algorithm)
        
**This is a game and should not be considered scientifically accurate or used as a diagnostic tool.



#Set Up informations
1)To ensure the project works on your PC, you need to install a [Chrome Driver](chromedriver.exe). The Chrome Driver must match the version of your installed Chrome browser. You can download it from the official website: [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads?hl=it).
This is required to implement the automatization of data-picking from a web page.
2)Clone the repository and place all files in the appropriate structure.
3)Install all the libraries 



#extra: I also included a [file](simulation_changing_csv.py) designed for testing the [webscraper](<landing page/webscraper.py>) by simulating new data. It allows you to delete specific lines from the CSV, making it possible to test the script's functionality without waiting a full week for updated data.)