import streamlit as st
from langchain_huggingface import HuggingFacePipeline
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('HUGGING_FACE_TOKEN')

def clear_history():
    st.session_state.messages = []



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


st.title('Your regular chatter')

if not 'messages' in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if not 'llm' in st.session_state:
    st.session_state.llm = llm

user_input = st.text_input('You: ', key='user_input')
st.sidebar.button('Clear Chat History', on_click=clear_history)

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = st.session_state.llm.invoke(user_input)
        full_response += assistant_response
        message_placeholder.markdown(full_response + '▌')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})