from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv
import os


load_dotenv()
keys = os.getenv("HUGGING_FACE_TOKEN")

llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation",
    model_kwargs={
        'temperature':0.7,
        "max_length": 400,
        "do_sample": True,
        "pad_token_id": 50256
    },
)

buffer_memory = ConversationBufferMemory()
summary_memory = ConversationSummaryMemory(llm=llm)

def run_convo(user_input):
    summary = summary_memory.load_memory_variables({})['summary']
    buffer = buffer_memory.load_memory_variables({})['history']

    context = f'Current Summary: {summary}\nPast conversation: {buffer}\nUser: {user_input}\nChatbot:'

    response = llm.invoke(user_input)

    buffer_memory.save_context({"input": user_input}, {"output": response})
    summary_memory.save_context({"input": user_input}, {"output": response})

    return response


print(run_convo("Hi, I want to plan a trip."))