from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from huggingface_hub import login
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import torch

from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)


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
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

        self.chathistory = None

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_response(self, user_input):
        try:
            new_user_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token, 
                return_tensors='pt'
            )
            
            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            else:
                bot_input_ids = new_user_input_ids

            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids, 
                    max_length=1000,
                    num_beams=5,
                    no_repeat_ngram_size=3,
                    do_sample=True,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    temperature=0.7,
                    top_p=0.9
                )

            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            )
            
            # Clean up the response
            response = response.strip()
            
            # If response is empty, provide a fallback
            if not response:
                response = "I'm not sure how to respond to that. Could you try rephrasing?"
                
            return response
        except Exception as e:
            return f"I'm having trouble processing that. Error: {str(e)}"
    
    def clear_history(self):
        self.chat_history_ids = None


chatbot = ChatBot()
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

        
        response = chatbot.generate_response(user_input)
        return response
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/clear', methods=['POST'])
def clear():
    chatbot.clear_history()
    return 'Chat history cleared.'

if __name__ == '__main__':
    app.run(debug=True)