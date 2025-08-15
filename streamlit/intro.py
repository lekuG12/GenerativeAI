import streamlit as st
import pandas as pd
from PIL import Image

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

#Button
if st.button('Say Hello'):
    st.write('say hello')

#checkbox
agree = st.checkbox('I agree')

#Radio button

genre = st.radio(
    'What is your favourite movie genre?',
    ('Comedy', 'Drama', 'Romance')
)

#Slider

age = st.slider('How old are you?', 0, 130, 25)
st.write(f'I am {age} years old')

#Text input

title = st.text_input('Movie title')
st.write('The current movie is', title)

#working with Images
image = Image.open('example.png')
st.image(image, caption='Riley and Robert Freeman')