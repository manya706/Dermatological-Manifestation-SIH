import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('predictions.csv')

disease_color_palette = px.colors.qualitative.Plotly
disease_to_color = {disease: color for disease, color in zip(df['Prediction'].unique(), disease_color_palette)}

st.sidebar.title("Monitoring System")

selected_page = st.sidebar.selectbox("Select a Page", ["Request Time Graph", "Diseases by Pincode"])

st.title("Monitoring System Visualization")

# Page: Request Time Graph
if selected_page == "Request Time Graph":
    st.write('\n\n')
    st.header("Request Time Graph")

    fig_time_line = px.line(df, x=df.index, y='Total Time (ms)', title='Request Time Line Plot')
    st.plotly_chart(fig_time_line)

    fig_time = px.histogram(df, x='Total Time (ms)', nbins=20, title='Request Time Histogram')
    st.plotly_chart(fig_time)

# Page: Diseases by Pincode
elif selected_page == "Diseases by Pincode":
    st.write('\n\n')
    st.header("Diseases by Pincode")

    pincode = st.text_input("Enter Pincode", "")
    pincode = int(pincode) if pincode.isdigit() and len(pincode) == 6 else None

    if pincode is not None:
        filtered_data = df[df['Pincode'] == pincode]
        if not filtered_data.empty:
            fig_histogram = px.histogram(filtered_data, x='Prediction', title=f'Diseases for Pincode: {pincode}')
            st.plotly_chart(fig_histogram)
        else:
            st.info("No data available for the entered pincode.")
    else:
        st.info("Please enter a valid 6-digit numeric pincode.")
