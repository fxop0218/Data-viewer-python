import pandas as pd
import plotly.express as px
import streamlit as srl

CITY = "City"
CUSTOMER_TYPE = "Customer_type"
GENDER = "Gender"

srl.set_page_config(page_title="Sales dashborad",
                    page_icon=":bar_chart:",
                    layout="wide")

# noinspection PyTypeChecker
df_mkt = pd.read_excel(
    engine="openpyxl",
    io="supermarkt.xlsx",
    sheet_name="Sales",
    usecols="B:R",
    nrows=1000,
    skiprows=3,
)
# Filter in the sidebar

srl.sidebar.header("Filter")
city = srl.sidebar.multiselect(f"Select the {CITY}",
                               options=df_mkt[CITY].unique(),
                               default=df_mkt[CITY].unique()
                               )
gender = srl.sidebar.multiselect(f"Select the {GENDER}:",
                                 options=df_mkt[GENDER].unique(),
                                 default=df_mkt[GENDER].unique()
                                 )
custom_type = srl.sidebar.multiselect(f"Select the {CUSTOMER_TYPE}:",
                                      options=df_mkt[CUSTOMER_TYPE].unique(),
                                      default=df_mkt[CUSTOMER_TYPE].unique()
                                      )

df_selection = df_mkt.query(
    f"City == @city & Customer_type == @custom_type & Gender == @gender"
)

srl.dataframe(df_selection)

srl.title(":bar_chart: Sales Dashboard")
srl.markdown("##")

total_sales = int(df_selection["Total"].sum())
avg_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(avg_rating, 0))
avg_sale_x_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = srl.columns(3)
with left_column:
    srl.subheader("Total sales")
    srl.subheader(f"US $ {total_sales:,}")
with middle_column:
    srl.subheader("Avarage rating")
    srl.subheader(f"{avg_rating} / {star_rating}")
with right_column:
    srl.subheader("Avarage sale x transaction")
    srl.subheader(f"US $ {avg_sale_x_transaction}")

srl.markdown("---")
