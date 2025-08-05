from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)
from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)

llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    pipeline_kwargs= dict(
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.2
    )
)

chat_model = ChatHuggingFace(llm=llm)

promting = input("Enter your prompt: ")
messages = [
    SystemMessage(content="You are a helpful assistant that answers questions about historical events."),
    HumanMessage(content=promting)
]

ai_msg = chat_model.invoke(messages)

print(ai_msg.content)  # Output: Marie Curie was a Polish-born physicist and chemist who conducted pioneering research on radioactivity