from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from dotenv import load_dotenv
import torch
import os

load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)

class ChatBot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-1B-distill")
        self.model = AutoModelForCausalLM.from_pretrained("facebook/blenderbot-1B-distill")
        self.chat_history_ids = None
        
        # Add padding token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_response(self, user_input):
        try:
            # Encode user input
            new_user_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token, 
                return_tensors='pt'
            )

            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            else:
                bot_input_ids = new_user_input_ids

            # Generate response
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

            # Decode response
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

# Initialize the chatbot
chatbot = ChatBot()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.form['user_message']

        if user_input.lower() in ['exit', 'quit', 'stop', 'bye']:
            return 'Goodbye! Thanks for chatting.'

        response = chatbot.generate_response(user_input)
        return response
    
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/clear', methods=['POST'])
def clear():
    chatbot.clear_history()
    return 'Chat history cleared.'

if __name__ == '__main__':
    app.run(debug=True)