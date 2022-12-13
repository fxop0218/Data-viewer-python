import pandas as pd
import plotly.express as px
import streamlit as srl

CITY = "City"
CUSTOMER_TYPE = "Customer_type"
GENDER = "Gender"

srl.set_page_config(page_title="Sales dashborad",
                    page_icon="🛒",
                    layout="wide")


# noinspection PyTypeChecker
@srl.cache
def get_excel_data():
    df = pd.read_excel(
        engine="openpyxl",
        io="supermarkt.xlsx",
        sheet_name="Sales",
        usecols="B:R",
        nrows=1000,
        skiprows=3,
    )
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df


df_mkt = get_excel_data()
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

srl.title(":bar_chart: 🛒 Sales Dashboard")
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

sales_x_prd = (df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total"))
fig_product_sales = px.bar(
    sales_x_prd,
    x="Total",
    y=sales_x_prd.index,
    orientation="h",
    title="<b>Sales x product</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_x_prd),
    template="plotly_white",
)
# SALES X HOUR

sales_x_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hour_sales = px.bar(
    sales_x_hour,
    x=sales_x_hour.index,
    y="Total",
    title="<b>Sales x hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_x_prd),
    template="plotly_white",
)
fig_hour_sales.update_layout(
    xaxis=dict(tickmode="linear"),
)

left_column, right_column = srl.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hour_sales, use_container_width=True)
srl.dataframe(df_selection)
hide_srl = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""

srl.markdown(hide_srl, unsafe_allow_html=True)
