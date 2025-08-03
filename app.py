import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# App title
st.title("U.S. Dog Market Finder")
st.markdown("Search and rank ZIP codes by estimated dog training potential.")

# Sidebar filters
st.sidebar.header("Filters")
zip_input = st.sidebar.text_input("Search by ZIP, City, or State")
min_income = st.sidebar.slider("Min Median Income ($)", 20000, 200000, 60000)
min_score = st.sidebar.slider("Min Market Score", 0, 100, 50)
min_dogs = st.sidebar.slider("Min Trainable Dogs", 0, 20000, 1000)

# Filter logic
filtered = df[
    (df["Median Income ($)"] >= min_income) &
    (df["Est. Trainable Dogs"] >= min_dogs) &
    (df["Market Score (0-100)"] >= min_score)
]

if zip_input:
    zip_input_lower = zip_input.lower()
    filtered = filtered[
        filtered["ZIP Code"].astype(str).str.contains(zip_input_lower) |
        filtered["City"].str.lower().str.contains(zip_input_lower) |
        filtered["State"].str.lower().str.contains(zip_input_lower)
    ]

# Display results
st.markdown(f"### {len(filtered)} ZIP codes match your criteria")
st.dataframe(filtered.sort_values("Market Score (0-100)", ascending=False))

# Download
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_dog_market_data.csv",
    mime="text/csv"
)  
