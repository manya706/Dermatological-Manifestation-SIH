import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the CSV data
df = pd.read_csv('predictions.csv')

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

fig_time_line = go.Figure()
fig_time_line.add_trace(
    go.Scatter(
        x=df.index,
        y=df['Total Time (ms)'],
        mode='lines',
        name='Request Time',
        line=dict(color='blue')
    )
)
fig_time_line.update_layout(
    title='Request Time Line Plot',
    xaxis_title='Index',
    yaxis_title='Total Time (ms)'
)
st.plotly_chart(fig_time_line)


fig_time = px.histogram(df, x='Total Time (ms)', nbins=20, title='Request Time Histogram')
st.plotly_chart(fig_time)

# Filter out rows with missing pincode or prediction
df_filtered = df.dropna(subset=['Pincode', 'Prediction'])

# Group by pincode and prediction, count occurrences
df_grouped = df_filtered.groupby(['Pincode', 'Prediction']).size().reset_index(name='Count')

# Create a density map
disease_to_color = {
    'Acne, or Rosacea': 'blue',
    'Actinic Keratosis, or other Malignant Lesions': 'green',
    'Alopecia, or other Hair Diseases': 'red',
    'Atopic Dermatitis': 'purple',
    'Bacterial Infections': 'orange',
    'Benign Tumors': 'pink',
    'Bullous Disease': 'brown',
    'Connective Tissue Diseases': 'gray',
    'Eczema': 'cyan',
    'Exanthems, or Drug Eruptions': 'magenta',
    'Fungal Infections': 'yellow',
    'Healthy or Benign growth': 'lime',
    'Herpes, HPV, other STDs': 'teal',
    'Lyme Diseasem, Infestations and Bites': 'olive',
    'Melanoma Skin Cancer Nevi and Moles': 'navy',
    'Nail Fungus or other Nail Disease': 'maroon',
    'Poison Ivy or Contact Dermatitis': 'gold',
    'Psoriasis, Lichen Planus or related diseases': 'purple',
    'Systemic Disease': 'lime',
    'Urticaria Hives': 'cyan',
    'Vascular Tumors': 'fuchsia',
    'Vasculitis Photos': 'royalblue',
    'Warts, or other Viral Infections': 'violet'
}
df_grouped['Color'] = df_grouped['Prediction'].apply(lambda disease: disease_to_color.get(disease, 'gray'))

india_lat = 20.5937
india_lon = 78.9629

st.header("Density Map of India using Pincode and Prediction")
fig_map = go.Figure()

# Loop through each disease and add a trace for it
for disease, color in disease_to_color.items():
    filtered_data = df_grouped[df_grouped['Prediction'] == disease]
    fig_map.add_trace(
        go.Densitymapbox(
            lat=,  # Use Pincode for latitude
            lon=,  # Use Prediction for longitude
            z=filtered_data['Count'],
            radius=50,
            colorscale='Viridis',
            colorbar=dict(
                title='Density',
                thickness=20,
            ),
            name=disease,
            hoverinfo='all',
            showscale=False,
            visible=True
        )
    )

fig_map.update_layout(
    mapbox_style="carto-positron",
    mapbox_center=dict(
        lat=india_lat,
        lon=india_lon
    ),
    mapbox_zoom=4,
)


# Add a dropdown to select the disease to display
disease_options = [disease for disease in disease_to_color.keys()]
disease_dropdown = st.selectbox('Select Disease:', disease_options, index=0)
for i in range(len(fig_map.data)):
    fig_map.data[i].visible = False
fig_map.data[disease_options.index(disease_dropdown)].visible = True

st.plotly_chart(fig_map)

# Display legend for disease colors
st.subheader("Disease Colors")
for disease, color in disease_to_color.items():
    st.markdown(f'<span style="color:{color}">■</span> {disease}', unsafe_allow_html=True)
