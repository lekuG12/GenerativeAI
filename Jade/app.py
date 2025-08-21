import os 
from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.tools import Tool
import datetime
from langchain_ollama.llms import OllamaLLM

load_dotenv()

tools = load_tools(['google-search'])
llm = OllamaLLM(model="qwen3:4b")


reminders = []

def setReminders(task: str) -> str:
    '''Sets a reminder for a given task'''

    reminders.append({'task': task, 'time':datetime.datetime.now()})
    return f'Reminder set for {task}.'


reminder_tool = Tool(
    name='Set reminder',
    func=setReminders,
    description='This tool is useful for creating reminders where the input should be the full description of the task.'
)

search_tool = tools[0]


