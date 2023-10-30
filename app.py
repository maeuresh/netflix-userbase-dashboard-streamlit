import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Netflix Userbase Dashboard", page_icon=":bar_chart:",
	layout="wide")

age_bins = [0,10, 20,30, 40,50, 60,70,80,90,100, float("inf")]
age_labels = ["0-10", "11-20", "21-30", "31-40","41-50","51-60","61-70","71-80","81-90","91-100"]

@st.cache_data
def get_data_from_excel():
	df = pd.read_csv("Netflix Userbase.csv")
	return df

df = get_data_from_excel()

def categorize_age(age):
    for i in range(len(age_bins) - 1):
        if age_bins[i] <= age < age_bins[i+1]:
            return age_labels[i]
    return "Unknown"

df["Age_Group"] = df["Age"].apply(categorize_age)

#-----SIDEBAR-----
st.sidebar.header("Please Select Your Filter(s) Here:")
device = st.sidebar.multiselect(
	"Select Device:",
	options=df["Device"].unique(),
	default=df["Device"].unique())

subscription_type = st.sidebar.multiselect(
	"Select Subscription Type:",
	options=df["Subscription_Type"].unique(),
	default=df["Subscription_Type"].unique())

gender = st.sidebar.multiselect(
	"Select Gender:",
	options=df["Gender"].unique(),
	default=df["Gender"].unique())

df_selection = df.query(
	"Device == @device & Subscription_Type == @subscription_type & Gender == @gender")

#-----MAIN PAGE-----
st.title(":bar_chart: Netflix Userbase Dashboard")
st.markdown('##')

#TOP ROW
total_revenue = int(df_selection["Monthly_Revenue"].sum())
average_age = round(df_selection["Age"].mean(),1)
average_revenue = round(df_selection["Monthly_Revenue"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
	st.subheader("Total Revenue:")
	st.subheader(f":heavy_dollar_sign: {total_revenue:,}")
with middle_column:
	st.subheader("Average Age:")
	st.subheader(f"{average_age:} Years")	
with right_column:
	st.subheader("Average Revenue:")
	st.subheader(f":heavy_dollar_sign: {average_revenue:}")

st.markdown("---")

revenue_by_countries = df_selection.groupby(by=["Country"]).sum()[["Monthly_Revenue"]].sort_values(by="Monthly_Revenue")

fig_total_monthly_revenue = px.bar(
	revenue_by_countries,
	x="Monthly_Revenue",
	y=revenue_by_countries.index,
	orientation="h",
	title="<b>Total Monthly Revenue By Countries</b>",
	color_discrete_sequence=["#4cc9f0"] * len(revenue_by_countries),
	template="plotly_white",)

#For removing bg and gridlines from chart
fig_total_monthly_revenue.update_layout(
	plot_bgcolor="rgba(0,0,0,0)",
	xaxis=(dict(showgrid=False)))


revenue_by_age_group = df.groupby("Age_Group").sum()[["Monthly_Revenue"]].sort_values(by="Age_Group")

fig_total_monthly_revenue_by_age = px.bar(
    revenue_by_age_group,
    x="Monthly_Revenue",
    y=revenue_by_age_group.index,
    orientation="h",
    title="<b>Total Monthly Revenue By Age Group</b>",
    color_discrete_sequence=["#4cc9f0"] * len(revenue_by_age_group),
    template="plotly_white"
)

# For removing bg and gridlines from chart
fig_total_monthly_revenue_by_age.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

left_column, right_column =st.columns(2)
left_column.plotly_chart(fig_total_monthly_revenue, use_container_width=True)
right_column.plotly_chart(fig_total_monthly_revenue_by_age, use_container_width=True)



#-----HIDING STREAMLIT UI------
hide_st_style = """<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html = True)
