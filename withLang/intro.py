import streamlit as st
from langchain_huggingface import HuggingFacePipeline
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('HUGGING_FACE_TOKEN')

st.set_page_config(
    page_title='Lanchain + Streamlit',
    page_icon=':robot'
)

llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.2,
        pad_token_id=50256  # Add padding token
    )
)

def generation(prompt):
    try:
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f'Error generating a response: {e}'


if 'responses' not in st.session_state:
    st.session_state.responses = []

# Title and introduction
st.title("Langchain + Streamlit Demo")
st.write("A simple demo of integrating Langchain with Streamlit.")

# Simple text input
user_input = st.text_input("Enter your prompt:")

if st.button('Generate'):
    if key:
        response = generation(user_input)
        st.write('Response: ', response)
    else:
        st.error("HuggingFace API Key not found. Please add it to your .env file.")


st.write('## Responses: ')
for i, message in enumerate(st.session_state.responses):
    st.write(f"**Prompt {i+1}:** {message['prompt']}")
    st.write(f"**Response {i+1}:** {message['response']}")
    st.write("---")