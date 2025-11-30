import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Data Dashboard")

# -----------------------------
# Upload File
# -----------------------------
uploaded_file = st.file_uploader("📁 Upload Netflix Dataset (.xlsx or .csv)", type=["xlsx", "csv"])

if uploaded_file is None:
    st.warning("Please upload your dataset file to continue.")
    st.stop()

# -----------------------------
# Read File Safely
# -----------------------------
file_name = uploaded_file.name.lower()

try:
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        # Convert xlsx → CSV in memory (NO openpyxl needed)
        excel_data = pd.ExcelFile(uploaded_file)
        sheet_name = excel_data.sheet_names[0]  # First sheet
        df = excel_data.parse(sheet_name)

except Exception as e:
    st.error(f"❌ Failed to read file: {e}")
    st.stop()

st.success("✅ File loaded successfully!")

# -----------------------------
# Filters
# -----------------------------
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

st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# -----------------------------
# Charts
# -----------------------------
import matplotlib.pyplot as plt

# Chart 1
st.subheader("🎥 Count of Movies vs TV Shows")
type_counts = df["type"].value_counts()

fig1, ax1 = plt.subplots()
ax1.bar(type_counts.index, type_counts.values)
st.pyplot(fig1)

# Chart 2
st.subheader("⏳ Content Added Over Time")
df["year_added"] = pd.to_datetime(df["date_added"], errors="coerce").dt.year
year_counts = df["year_added"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.plot(year_counts.index, year_counts.values)
st.pyplot(fig2)

# Chart 3
st.subheader("🎭 Top Genres")
df["genres"] = df["listed_in"].apply(lambda x: x.split(",")[0] if pd.notnull(x) else "Unknown")
genre_counts = df["genres"].value_counts().head(10)

fig3, ax3 = plt.subplots()
ax3.barh(genre_counts.index, genre_counts.values)
st.pyplot(fig3)

st.markdown("---")
st.caption("Made by Vaishnavi — Netflix Dashboard using Streamlit")
