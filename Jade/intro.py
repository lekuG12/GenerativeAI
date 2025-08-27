import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
import os
from dotenv import load_dotenv

load_dotenv()

def clear_history():
    st.session_state.messages = []


search_tools = load_tools(['google-search'])
llm = OllamaLLM(model="qwen3:4b")  # Fixed model name


agent = initialize_agent(
    tools=search_tools, 
    llm=llm, 
    agent='zero-shot-react-description', 
    verbose=False
)


st.title('Your regular chatter')

if not 'messages' in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if not 'agent' in st.session_state:
    st.session_state.agent = agent

user_input = st.text_input('You: ', key='user_input')
st.sidebar.button('Clear Chat History', on_click=clear_history)

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = st.session_state.agent.run(user_input)
        full_response += assistant_response
        message_placeholder.markdown(full_response + '▌')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})