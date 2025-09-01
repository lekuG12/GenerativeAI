import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
import os
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain.schema import LLMResult
from langchain.llms.base import LLM
from pydantic import PrivateAttr


class CleanerLLM(LLM):
    # Use PrivateAttr to store non-pydantic fields
    _llm: LLM = PrivateAttr()

    def __init__(self, llm: LLM, **kwargs):
        super().__init__(**kwargs)
        self._llm = llm

    @property
    def _llm_type(self):
        return 'cleaned'
    
    def _call(self, prompt, stop=None):
        raw_output = self._llm.invoke(prompt)
        import re
        cleaned = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        return cleaned.strip()
    
    async def _acall(self, prompt, stop=None):
        raw_output = await self._llm.ainvoke(prompt)
        import re
        cleaned = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        return cleaned.strip()
    


load_dotenv()

def clear_history():
    # Ensure messages is initialized
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    else:
        st.session_state.messages.clear()

memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
search_tools = load_tools(['google-search'])
llm = CleanerLLM(OllamaLLM(model="qwen3:4b"))  # Fixed model name

if 'agent' not in st.session_state:
    st.session_state.agent = initialize_agent(
        tools=search_tools, 
        llm=llm, 
        agent='conversational-react-description', 
        memory=memory,
        verbose=False,
        handle_parsing_errors=True
    )

st.title('Sensei237')

if 'messages' not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.text_input('You: ', key='user_input')
st.sidebar.button('Clear Chat History', on_click=clear_history)

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ''
        response = st.session_state.agent.invoke({'input': user_input})
        assistant_response = response.get("output", str(response))
        full_response += assistant_response
        message_placeholder.markdown(full_response + '▌')
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})