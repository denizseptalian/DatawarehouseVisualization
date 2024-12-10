import streamlit as st
import folium
import pandas as pd
import streamlit.components.v1 as components

# Function to load data from Excel or CSV
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        st.error("File harus berformat .csv atau .xlsx")
        return None
# Streamlit interface
st.write("""
    Aplikasi ini menampilkan peta interaktif dengan lokasi yang dikategorikan berdasarkan potensi.
    Setiap lokasi ditandai dengan warna marker yang berbeda sesuai dengan kategorinya.
""")
# Default data
data = {
    'Lokasi': [
        "Blmngtn", "Blueste", "BrDale", "BrkSide", "ClearCr", "CollgCr", "Crawfor", "Edwards", "Gilbert",
        "Greens", "GrnHill", "IDOTRR", "Landmrk", "MeadowV", "Mitchel", "NAmes", "NoRidge", "NPkVill", "NridgHt",
        "NWAmes", "OldTown", "Sawyer", "SawyerW", "Somerst", "StoneBr", "SWISU", "Timber", "Veenker"
    ],
    'Kategori_Potensi': [
        "Sangat Potensial", "Sangat Potensial", "Berpotensial", "Berpotensial", "Sangat Potensial", "Sangat Potensial",
        "Berpotensial", "Berpotensial", "Sangat Potensial", "Sangat Potensial", "Sangat Potensial", "Berpotensial",
        "Sangat Potensial", "Berpotensial", "Sangat Potensial", "Sangat Potensial", "Sangat Potensial", "Sangat Potensial",
        "Sangat Potensial", "Sangat Potensial", "Sangat Potensial", "Sangat Potensial", "Berpotensial", "Sangat Potensial",
        "Berpotensial", "Sangat Potensial", "Sangat Potensial", "Sangat Potensial"
    ],
    'Latitude': [
        42.0334, 42.0370, 42.0192, 42.0255, 42.0321, 42.0298, 42.0167, 42.0303, 42.0173,
        42.0212, 42.0221, 42.0296, 42.0323, 42.0157, 42.0291, 42.0295, 42.0299, 42.0288, 42.0283,
        42.0241, 42.0304, 42.0223, 42.0240, 42.0315, 42.0194, 42.0281, 42.0263, 42.0312
    ],
    'Longitude': [
        -93.6177, -93.6136, -93.6259, -93.6120, -93.6173, -93.6244, -93.6325, -93.6187, -93.6067,
        -93.6138, -93.6265, -93.6249, -93.6141, -93.6094, -93.6155, -93.6181, -93.6202, -93.6126, -93.6190,
        -93.6282, -93.6123, -93.6250, -93.6235, -93.6169, -93.6184, -93.6133, -93.6148, -93.6164
    ]
}

# Default DataFrame
df = pd.DataFrame(data)

# Streamlit interface
st.title("Peta Lokasi Potensi")

# Upload file
uploaded_file = st.file_uploader("Unggah file data (Excel/CSV)", type=["csv", "xlsx"])

# If file is uploaded, load it and display the new data
if uploaded_file is not None:
    new_df = load_data(uploaded_file)
    if new_df is not None:
        # Ensure the new data has the correct columns
        required_columns = ['Lokasi', 'Kategori_Potensi', 'Latitude', 'Longitude']
        if all(col in new_df.columns for col in required_columns):
            df = new_df
            st.success("Data berhasil dimuat!")
        else:
            st.error(f"Data harus memiliki kolom: {', '.join(required_columns)}")

# Function to assign marker color based on kategori
def get_marker_color(kategori):
    if kategori == "Sangat Potensial":
        return 'green'
    elif kategori == "Berpotensial":
        return 'orange'
    else:
        return 'blue'

# Create map centered at Ames, Iowa
m = folium.Map(location=[42.0297, -93.6177], zoom_start=13)

# Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Lokasi']}: {row['Kategori_Potensi']}",
        icon=folium.Icon(color=get_marker_color(row['Kategori_Potensi']))
    ).add_to(m)

# Save the map to an HTML file (temporary location)
m.save("map_potensi_lokasi.html")

# Display the map in Streamlit using the HTML component
with open("map_potensi_lokasi.html", "r") as file:
    map_html = file.read()

components.html(map_html, height=600)

# Optionally, display the dataframe below the map
st.subheader("Data Lokasi dan Potensi")
st.dataframe(df)
