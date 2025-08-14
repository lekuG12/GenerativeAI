from langchain.agents import AgentType, initialize_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv
import os

load_dotenv()
hf_token = os.getenv("HUGGING_FACE_TOKEN")

llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation",
    model_kwargs={
        'temperature': 0.7,
        "max_length": 400,
        "do_sample": True,
        "pad_token_id": 50256
    }
)
wiki_wrapper = WikipediaAPIWrapper()
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
tools = [wiki]

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

response = agent.run('Tell me about the history of the Eiffel Tower')
print(response)