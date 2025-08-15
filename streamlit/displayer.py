import streamlit as st
import pandas as pd

st.title('Displayer')

df = st.file_uploader('Upload your document', type=['xlsx'])

pd_value = pd.read_excel(df)
X = pd_value['Predicted Disease']
Y = pd_value['Temperature Alert']

plot_df = pd.DataFrame({
    'Predicted Disease': X,
    'Temperature Alert': Y
})

st.line_chart(plot_df)
