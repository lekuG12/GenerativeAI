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
    model_id="facebook/blenderbot-400M-distill",
    task="text-generation",
    pipeline_kwargs= dict(
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.2
    )
)

chat_model = ChatHuggingFace(llm=llm)


messages = [
    SystemMessage(content="You are a helpful assistant. You can answer questions and engage in conversation."),
]

while True:
    user_input = input("\nYOU:  ")

    if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
        print("Exiting the chat.")
        break


    messages.append(HumanMessage(content=user_input))
    ai_msg = chat_model.invoke(messages)

    print(f"Bot: {ai_msg.content}")
