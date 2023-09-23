import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV data
df = pd.read_csv('Backend/predictions.csv')

# Define a color palette for diseases
disease_color_palette = px.colors.qualitative.Plotly

# Map diseases to colors
disease_to_color = {disease: color for disease, color in zip(df['Prediction'].unique(), disease_color_palette)}

# Sidebar title
st.sidebar.title("Monitoring System")

# Main content
st.title("Monitoring System Visualization")

# Plot request time graph
st.header("Request Time Graph")
fig_time = px.histogram(df, x='Total Time (ms)', nbins=20, title='Request Time Histogram')
st.plotly_chart(fig_time)

# Filter out rows with missing pincode or prediction
df_filtered = df.dropna(subset=['Pincode', 'Prediction'])

# Group by pincode and prediction, count occurrences
df_grouped = df_filtered.groupby(['Pincode', 'Prediction']).size().reset_index(name='Count')

# Create a density map
st.header("Density Map of India using Pincode and Prediction")
fig_map = px.density_mapbox(df_grouped,
                            lat=df_grouped['Pincode'].astype(float),
                            lon=df_grouped['Prediction'].astype(float),
                            z=df_grouped['Count'],
                            color_discrete_map=disease_to_color,  # Assign colors to diseases
                            radius=10,
                            center=dict(lat=20, lon=78),
                            zoom=4,
                            mapbox_style="carto-positron",
                            title="Density Map of India using Pincode and Prediction")
st.plotly_chart(fig_map)

# Display legend for disease colors
st.subheader("Disease Colors")
for disease, color in disease_to_color.items():
    st.markdown(f'<span style="color:{color}">■</span> {disease}', unsafe_allow_html=True)
