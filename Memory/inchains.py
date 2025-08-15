from langchain.chains import ConversationChain
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

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

print(conversation.predict(input="Hi, my name is John."))
print(conversation.predict(input="Hi, what is my name."))