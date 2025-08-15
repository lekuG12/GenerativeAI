import time
import streamlit as st

@st.cache_data
def hardComputation(param):
    time.sleep(5)
    return param * 2

value = st.number_input('Enter a number', value=1)
results = hardComputation(value)
st.write(f'Result: {results}')