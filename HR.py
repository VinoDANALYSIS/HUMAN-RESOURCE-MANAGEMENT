# Import required libraries
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px

st.set_page_config(page_title="Industrial Human Resource Management",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Function to load and preprocess data
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Clean and preprocess column names
        df.columns = df.columns.str.strip().str.lower()
        return df
    else:
        st.error(f"File not found at path: {file_path}")
        return None

# Load the dataset
file_path = 'C:/Users/hp/Desktop/INDUSTRIAL HUMAN RESOURCE MANAGEMENT/human_resource2.csv' # Update with your actual path
df = load_data(file_path)

if df is not None:

    st.title("Industrial Human Resource Management")
    # Sidebar filters: State and NIC Name (Industry)
    st.sidebar.header("Filters")
    selected_state = st.sidebar.selectbox("Select State", df['state name'].unique())
    selected_nic_name = st.sidebar.selectbox("Select Industry (NIC Name)", df['nic name'].unique())

    # Filter data based on selection
    filtered_data = df[(df['state name'] == selected_state) & (df['nic name'] == selected_nic_name)]
    
    # Summarize the Main workers data for the selected filters
    total_main_workers = filtered_data['main workers - total -  persons'].sum()
    rural_main_workers = filtered_data['main workers - rural -  persons'].sum()
    urban_main_workers = filtered_data['main workers - urban -  persons'].sum()

    # Summarize marginal workers data
    total_marginal_workers = filtered_data['marginal workers - total -  persons'].sum()
    rural_marginal_workers = filtered_data['marginal workers - rural -  persons'].sum()
    urban_marginal_workers = filtered_data['marginal workers - urban -  persons'].sum()

    st.header(f"Industrial Human Resource Management in {selected_state}")
    st.subheader(f"Industry: {selected_nic_name}")

    # Display total Main workers data
    st.write(f"**Total Workers in {selected_state}:** {total_main_workers}")
    st.write(f"**Rural Workers:** {rural_main_workers}")
    st.write(f"**Urban Workers:** {urban_main_workers}")

    st.write(f"**Marginal Workers in {selected_state}:** {total_marginal_workers}")
    st.write(f"**Rural Marginal Workers:** {rural_marginal_workers}")
    st.write(f"**Urban Marginal Workers:** {urban_marginal_workers}")
    
    # Plotly Bar Chart: Main Workers vs Marginal Workers (Rural vs Urban)
    fig = px.bar(
        x=['Rural Main Workers', 'Urban Main Workers', 'Rural Marginal Workers', 'Urban Marginal Workers'],
        y=[rural_main_workers, urban_main_workers, rural_marginal_workers, urban_marginal_workers],
        labels={'x': "Worker Type", 'y': "Number of Workers"},
        title=f"Main vs Marginal Workers in {selected_state} ({selected_nic_name})"
    )
    st.plotly_chart(fig)

    # Plotly Pie Chart: Gender Distribution for Main and Marginal Workers
    total_main_male_workers = filtered_data['main workers - total - males'].sum()
    total_main_female_workers = filtered_data['main workers - total - females'].sum()

    total_marginal_male_workers = filtered_data['marginal workers - total - males'].sum()
    total_marginal_female_workers = filtered_data['marginal workers - total - females'].sum()

    fig2 = px.pie(
        values=[total_main_male_workers, total_main_female_workers, total_marginal_male_workers, total_marginal_female_workers],
        names=['Main Males', 'Main Females', 'Marginal Males', 'Marginal Females'],
        title=f"Gender Distribution for Main vs Marginal Workers in {selected_state} ({selected_nic_name})"
    )
    st.plotly_chart(fig2)

    # Folium Map: Display worker population geospatially by districts
    st.subheader(f"Worker Distribution by District in {selected_state}")

    # Create a base map
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Center on India

    # Add marker clusters for each district
    marker_cluster = MarkerCluster().add_to(map)

    # Group by district and get the total workers (Main + Marginal) per district
    district_data = filtered_data.groupby('district')[['main workers - total -  persons', 'marginal workers - total -  persons']].sum().reset_index()
    # Add each district's data to the map
    for _, row in district_data.iterrows():
        folium.Marker(
            location=[20.5937, 78.9629],  # Adjust this with actual latitude/longitude data
            popup=f"{row['district']}: {row['main workers - total -  persons']} Main Workers, {row['marginal workers - total -  persons']} Marginal Workers",
        ).add_to(marker_cluster)

    # Render the map in Streamlit
    folium_static(map)

    # Additional insights and facts
    st.subheader("Insights and Key Facts")
    st.write(f"1. The {selected_nic_name} industry in {selected_state} employs {total_main_workers} main workers and {total_marginal_workers} marginal workers in total.")
    st.write(f"2. The majority of main workers are {'rural' if rural_main_workers > urban_main_workers else 'urban'} based, while the majority of marginal workers are {'rural' if rural_marginal_workers > urban_marginal_workers else 'urban'} based.")
    st.write(f"3. Gender distribution shows {total_main_male_workers} main male workers and {total_marginal_male_workers} marginal male workers, and {total_main_female_workers} main female workers and {total_marginal_female_workers} marginal female workers.")

else:
    st.error("Data could not be loaded. Please check the file path or data format.")