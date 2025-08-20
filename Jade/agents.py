import streamlit as st
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"  # Replace with your actual API key

# Initialize LLM
llm = OpenAI(temperature=0)

# Initialize memory
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationSummaryMemory(llm=llm)

# Initialize conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state["memory"],
    verbose=True #Added for demonstration purposes
)

user_input = st.chat_input("Enter your query:")

if user_input:
    # Get response from the model
    response = conversation.predict(input=user_input)

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Display model response
    with st.chat_message("model"):
        st.write(response)