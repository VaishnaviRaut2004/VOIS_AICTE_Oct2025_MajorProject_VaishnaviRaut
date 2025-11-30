import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    return pd.read_csv("Netflix Dataset.csv", encoding="latin1", on_bad_lines="skip")

df = load_data()

st.title("📺 Netflix Data Dashboard")
st.write("Simple dashboard created using Streamlit")

# ---- Sidebar Filters ----
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].dropna().unique(),
    default=[]
)

# Apply filters
filtered_df = df[df["type"].isin(type_filter)]

if country_filter:
    filtered_df = filtered_df[filtered_df["country"].isin(country_filter)]

# ---- KPIs ----
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df["type"]=="Movie"]))
col3.metric("TV Shows", len(filtered_df[filtered_df["type"]=="TV Show"]))

st.markdown("---")

# ---- Charts ----

# 1. Count of Movies vs TV Shows
fig1 = px.histogram(filtered_df, x="type", title="Movies vs TV Shows")
st.plotly_chart(fig1, use_container_width=True)

# 2. Top 10 Countries with Most Titles
top_countries = filtered_df["country"].value_counts().head(10).reset_index()
top_countries.columns = ["country", "count"]

fig2 = px.bar(top_countries, x="country", y="count",
              title="Top 10 Countries with Most Titles")
st.plotly_chart(fig2, use_container_width=True)

# 3. Titles over the years
df_year = filtered_df.dropna(subset=["release_year"])
fig3 = px.line(df_year.groupby("release_year").size().reset_index(name='count'),
               x="release_year", y="count", title="Content Added Over the Years")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("Dashboard completed ✔")

