import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from urllib.request import urlopen
import json

# Оставляем только необходимые переменные
df = df[['iso_code','location','total_cases_per_million','total_deaths_per_million','people_vaccinated_per_hundred','date']]
df = df[df.location != 'World']
df["date"] = pd.to_datetime(df["date"])
# Сохраним данные в формате csv для создания приложения
df.to_csv('data.csv', index = False)

# Настройка заголовка и текста 
st.title("COVID 19 IN THE WORLD DASHBOARD")
st.write("""This dashboard will present the spread of COVID-19 in the world by visualizing the timeline of the total cases and deaths. As well as the total number of vaccinated people.""")

# Настройка боковой панели
st.sidebar.title("About")
st.sidebar.info(
    """
    This app is Open Source dashboard.
    """
)
st.sidebar.info("Feel free to collaborate and comment on the work. The github link can be found "
                "[here](https://github.com/yuliianikolaenko/COVID_dashboard_proglib).")
