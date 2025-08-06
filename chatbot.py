from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from huggingface_hub import login
from dotenv import load_dotenv
import os

from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)


llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/DialoGPT-medium",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.2,
        pad_token_id=50256  # Add padding token
    )
)

chat_model = ChatHuggingFace(llm=llm)

class ConversationManager:
    def __init__(self):
        self.messages = [
            SystemMessage(content="You are a helpful assistant. You can answer questions and engage in conversation."),
        ]

    def add_message(self, message):
        self.messages.append(message)
        # Keep conversation manageable
        if len(self.messages) > 11:
            self.messages = [self.messages[0]] + self.messages[-10:]

    def clear(self):
        self.messages = [
            SystemMessage(content="You are a helpful assistant. You can answer questions and engage in conversation."),
        ]

    def get_messages(self):
        return self.messages
    

class ChatBot:
    def __init__(self):
        self.conversation = ConversationManager()
    

conversation = ConversationManager()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def chat():
    try:
        user_input = request.form['user_message']

        if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
            return jsonify({'response': 'Goodbye! Thanks for chatting.'})

        
        user_message = HumanMessage(content=user_input)
        conversation.add_message(user_message)
        
        
        ai_msg = chat_model.invoke(conversation.get_messages())
        conversation.add_message(ai_msg)

        return ai_msg.content
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/clear', methods=['POST'])
def clear():
    conversation.clear()
    return 'Chat history cleared.'



if __name__ == '__main__':
    app.run(debug=True)