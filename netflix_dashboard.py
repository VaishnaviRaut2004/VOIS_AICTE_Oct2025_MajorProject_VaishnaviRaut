import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# -------------------------------------------
# Load Excel Data
# -------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Netflix Dataset.xlsx") 
    return df

df = load_data()

# Rename columns to lowercase for easy use
df.columns = df.columns.str.lower()

# -------------------------------------------
# Title
# -------------------------------------------
st.title("🎬 Netflix Data Dashboard")

# -------------------------------------------
# Sidebar Filters
# -------------------------------------------
st.sidebar.header("Filters")

# Filter: Category (Movie / TV Show)
category_options = ["All"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", category_options)

# Filter: Country
country_options = ["All"] + sorted(df["country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_options)

# Apply Filters
filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

# -------------------------------------------
# Display Filtered Data
# -------------------------------------------
st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# -------------------------------------------
# Chart 1: Movies vs TV Shows Count
# -------------------------------------------
st.subheader("🎥 Count of Movies vs TV Shows")

cat_counts = df["category"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(cat_counts.index, cat_counts.values)
ax1.set_title("Movies vs TV Shows")
ax1.set_xlabel("Category")
ax1.set_ylabel("Count")

st.pyplot(fig1)

# -------------------------------------------
# Chart 2: Content Released Over Years
# -------------------------------------------
st.subheader("⏳ Content Released Over the Years")

df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
year_counts = df["release_year"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(year_counts.index, year_counts.values, marker='o')
ax2.set_title("Content Released Over Time")
ax2.set_xlabel("Year")
ax2.set_ylabel("Count")

st.pyplot(fig2)

# -------------------------------------------
# Chart 3: Top 10 Categories (Type column)
# -------------------------------------------
st.subheader("🎭 Top 10 Types / Genres")

df["main_type"] = df["type"].apply(
    lambda x: x.split(",")[0] if pd.notnull(x) else "Unknown"
)
type_counts = df["main_type"].value_counts().head(10)

fig3, ax3 = plt.subplots()
ax3.barh(type_counts.index, type_counts.values)
ax3.set_title("Top 10 Types / Genres")
ax3.set_xlabel("Count")

st.pyplot(fig3)

# -------------------------------------------
# Footer
# -------------------------------------------
st.markdown("---")
st.caption("Made by Vaishnavi — Netflix Dashboard using Streamlit")
