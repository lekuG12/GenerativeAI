import os 
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools  # Updated import
from langchain.tools import Tool
import datetime
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent
import pyttsx3

load_dotenv()

search_tools = load_tools(['google-search'])
llm = OllamaLLM(model="qwen3:4b")  # Fixed model name

reminders = []

def text_to_speech(text: str) -> str:
    try: 
    
        engine = pyttsx3.init()
            
        # Optional: Set voice properties
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  # Female voice (index 1)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)
            
        engine.say(text)
        engine.runAndWait()
        print("Speech completed using Windows SAPI")
    except ImportError:
            print("pyttsx3 not installed. Run: pip install pyttsx3")
    except Exception as e:
            print(f"Error with Windows SAPI: {e}")




def setReminders(task: str) -> str:
    '''Sets a reminder for a given task'''
    reminders.append({'task': task, 'time': datetime.datetime.now()})
    return f'Reminder set for {task}.'


speak_tool = Tool(
      name='Talking response',
      func=text_to_speech,
      description='This tool is responsible for providing an audio response to the given model output'
)

reminder_tool = Tool(
    name='Set reminder',
    func=setReminders,
    description='This tool is useful for creating reminders where the input should be the full description of the task.'
)

# Fix: Properly combine the tools - extend the search_tools list with reminder_tool
all_tools = search_tools + [reminder_tool] + [speak_tool]

agent = initialize_agent(
    tools=all_tools, 
    llm=llm, 
    agent='zero-shot-react-description', 
    verbose=True
)

# Example usage
response = agent.run("What is the current population of Canada? Also, remind me to check the weather in 2 hours.")
print(response)