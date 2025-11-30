import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Load Dataset (No Upload Needed)
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Netflix Dataset.xlsx")

df = load_data()

# ------------------------------
# Dashboard Title
# ------------------------------
st.title("📊 Simple Netflix Dataset Dashboard")

# ------------------------------
# Show Dataset
# ------------------------------
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ------------------------------
# Visualization 1: Type Count
# ------------------------------
st.subheader("🎬 Count of Movies vs TV Shows")

type_counts = df["type"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(type_counts.index, type_counts.values)
ax1.set_xlabel("Type")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# ------------------------------
# Visualization 2: Top 10 Countries
# ------------------------------
st.subheader("🌎 Top 10 Countries with Most Titles")

df["country"] = df["country"].fillna("Unknown")
country_counts = df["country"].value_counts().head(10)

fig2, ax2 = plt.subplots()
ax2.barh(country_counts.index, country_counts.values)
ax2.set_xlabel("Count")
st.pyplot(fig2)

# ------------------------------
# Visualization 3: Release Years
# ------------------------------
st.subheader("📅 Distribution of Release Years")

fig3, ax3 = plt.subplots()
ax3.hist(df["release_year"].dropna(), bins=20)
ax3.set_xlabel("Release Year")
ax3.set_ylabel("Count")
st.pyplot(fig3)
