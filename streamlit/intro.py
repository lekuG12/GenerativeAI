import streamlit as st
import pandas as pd

st.title('This is my first streamlit application')
st.header('This is a header')
st.subheader('This is a subheader')

st.write('Hello, Streamlit')
st.markdown('**This is a bold text using a markdown**')

#Using dataframes

data = {'col1': [1, 2, 3], 'col2': [4, 5, 6]}
df = pd.DataFrame(data)

st.dataframe(df)
st.table(df)

st.json({'name': 'Streamlit', 'version': '1.0'})
st.metric(label="Temperature", value="70 °F", delta="1.2 °F")