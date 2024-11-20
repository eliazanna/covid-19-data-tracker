#historic covid series

import streamlit as st
from plots_functions import plot_europe_map
from plots_functions import death_case_ratio

st.set_page_config(page_title="COVID SERIES")
st.header("The effects of Covid-19 in Europe")

#selectbox per scegliere il grafico 1
option = st.selectbox('',('Total Cases per Million', 'Total Deaths per Million', 'Hospital Patients per Million'))

if option == 'Total Cases per Million':
    st.write("This map shows the total cases per million people in Europe, highlighting the spread of the virus across the continent.")
    fig3 = plot_europe_map(colonna='total_cases_per_million', cmap='OrRd', color_null=False) 
    st.pyplot(fig3)

elif option == 'Total Deaths per Million':
    st.write("This map displays the total deaths per million people in Europe, providing insight into the mortality impact.")
    fig4 = plot_europe_map(colonna='total_deaths_per_million', cmap='Greys', color_null=False)
    st.pyplot(fig4)

else:
    st.write("This map shows the number of hospital patients per million people in Europe, reflecting the pressure on the healthcare system.")
    fig5 = plot_europe_map(colonna='hosp_patients_per_million', cmap='Blues', color_null=True)
    st.pyplot(fig5)

st.markdown(  """ <hr style="border:0.6px solid #d3d3d3; margin-bottom: 15px; width: 100%;" />""", unsafe_allow_html=True )
#-------------------------------------------------------------------------------------

st.header("Trend of COVID-19 Mortality Rate in Italy")
st.write('')
#selectbox per il grafico 2
with_asintoti = st.checkbox("Compare with vaccinated population")
add_europa = st.checkbox("Compare with European average")

# Mostra il risultato basato sulle selezioni
if add_europa and with_asintoti:
    st.pyplot(death_case_ratio(add_europa=add_europa, with_asintoti=with_asintoti))
    st.write("Comparing with both the European average and the vaccinated population provides a comprehensive view of Italy's performance.")
    st.write("The comparison highlights how Italy fares relative to other European countries and evaluates the effectiveness of vaccination in reducing COVID-19 deaths.")
elif with_asintoti:
    st.pyplot(death_case_ratio(add_europa=add_europa, with_asintoti=with_asintoti))
    st.write("Comparing new deaths on new cases with the vaccinated population gives insight into the role of vaccination in mitigating the severity of COVID-19 in Italy.")
    st.write("This analysis emphasizes how the vaccination campaign impacts the ratio of new deaths to new cases over time.")
elif add_europa:
    st.pyplot(death_case_ratio(add_europa=add_europa, with_asintoti=with_asintoti))
    st.write("Comparing new deaths on new cases with the European average highlights Italy's position relative to its neighbors.")
    st.write("This comparison provides context on whether Italy is performing better or worse than the European average in terms of managing new COVID-19 cases and deaths.")
else:
    st.pyplot(death_case_ratio(add_europa=add_europa, with_asintoti=with_asintoti))
    st.write("No comparison selected. Displaying the default analysis for new deaths on new cases in Italy.")
    st.write("This baseline analysis focuses on trends within Italy without external comparisons, offering a clear view of the internal situation.")
# Mostra il grafico con i parametri definiti

