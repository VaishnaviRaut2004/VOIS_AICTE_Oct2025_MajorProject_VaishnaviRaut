import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# -------------------------------------------
# Load Excel Data (BEST FIX)
# -------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Netflix Dataset.xlsx")   # ← use XLSX

df = load_data()

# -------------------------------------------
# Title
# -------------------------------------------
st.title("🎬 Netflix Data Dashboard")

# -------------------------------------------
# Sidebar Filters
# -------------------------------------------
st.sidebar.header("Filters")

type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("Select Type", type_options)

country_options = ["All"] + sorted(df["country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_options)

filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

# -------------------------------------------
# Display Data
# -------------------------------------------
st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# -------------------------------------------
# Chart 1: Movies vs Shows
# -------------------------------------------
st.subheader("🎥 Count of Movies vs TV Shows")

type_counts = df["type"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(type_counts.index, type_counts.values)
ax1.set_title("Movies vs TV Shows")
st.pyplot(fig1)

# -------------------------------------------
# Chart 2: Year Added
# -------------------------------------------
st.subheader("⏳ Content Added Per Year")

df["year_added"] = pd.to_datetime(df["date_added"], errors="coerce").dt.year
year_counts = df["year_added"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(year_counts.index, year_counts.values, marker="o")
ax2.set_title("Content Added Over Time")
st.pyplot(fig2)

# -------------------------------------------
# Chart 3: Top Genres
# -------------------------------------------
st.subheader("🎭 Top 10 Genres")

df["genres"] = df["listed_in"].apply(
    lambda x: x.split(",")[0] if pd.notnull(x) else "Unknown"
)
genre_counts = df["genres"].value_counts().head(10)

fig3, ax3 = plt.subplots()
ax3.barh(genre_counts.index, genre_counts.values)
ax3.set_title("Top 10 Genres")
st.pyplot(fig3)

# -------------------------------------------
# Footer
# -------------------------------------------
st.markdown("---")
st.caption("Made by Vaishnavi — Netflix Dashboard")
