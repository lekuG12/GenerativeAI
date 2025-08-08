from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
from dotenv import load_dotenv
import os


load_dotenv()
keys = os.getenv("HUGGING_FACE_TOKEN")


topic = PromptTemplate.from_template('Suggest a topic for a short story')
llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    model_kwargs={
        'temperature':0.7,
        "max_length": 400,
        "do_sample": True,
        "pad_token_id": 50256
    },
)

topic_chain = topic | llm


#second model
story = PromptTemplate.from_template('Write a short story about {input}')
llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation",
    model_kwargs={
        "temperature":0.8,
        "max_length": 400,
        "do_sample": True,
        "pad_token_id": 50256,
    },
)
story_chain = story | llm

overall_chain = topic_chain | story_chain

input_text = 'Write a short story about a brave knight.'

story = overall_chain.invoke({'input': input_text})
print(f"Generated Story: {story}")
