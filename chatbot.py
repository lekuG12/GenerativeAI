from flask import Flask, render_template, request
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from huggingface_hub import login
from dotenv import load_dotenv
import os

from langchain.schema import (
    HumanMessage,
    SystemMessage,
    AIMessage,
)

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)


llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    while True:

        if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
            print("Exiting the chat.")
            break


        messages.append(HumanMessage(content=user_input))
        ai_msg = chat_model.invoke(messages)

        return ai_msg.content



if __name__ == '__main__':
    app.run(debug=True)