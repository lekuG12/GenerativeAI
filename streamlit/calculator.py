import streamlit as st

st.title('Simple Calculator')

num1 = st.number_input('Enter first input')
num2 = st.number_input('Enter second input')

operations = st.selectbox(
    'Choose and operation',
    ('Add', 'Subtract', 'Divide', 'Multiply')
    )


if operations == 'Add':
    results = num1+num2
    st.write(results)
elif operations == 'Divide':
    results = num1/num2
    st.write(results)
elif operations == 'Multiply':
    results = num1*num2
    st.write(results)
else:
    results = num1-num2
    st.write(results)