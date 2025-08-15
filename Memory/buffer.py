from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
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

memory = ConversationBufferMemory()

input_text = 'Hi, my name is John'
llm_response = llm.invoke(input_text)

memory.save_context({"input": input_text}, {"output": llm_response})
print(f"User: {input_text}")
print(f"AI: {llm_response}")


input_text = "What is my name?"
llm_response = llm.invoke(input_text)
memory.save_context({"input": input_text}, {"output": llm_response})
print(f"User: {input_text}")
print(f"AI: {llm_response}")
