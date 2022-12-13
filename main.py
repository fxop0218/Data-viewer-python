import pandas as pd
import plotly.express as px
import streamlit as srl

srl.set_page_config(page_title="Sales dashborad",
                    page_icon=":bar_chart:",
                    layout="wide")

df_mkt = pd.read_excel(
    io="supermarkt.xlsx",
    engine="openpyxl",
    sheet_name="Sales",
    skiprows=3,
    usecols="B:R",
    nrows=1000,
)

srl.dataframe(df_mkt)
