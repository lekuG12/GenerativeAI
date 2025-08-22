import os 
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools  # Updated import
from langchain.tools import Tool
import datetime
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent

load_dotenv()

search_tools = load_tools(['google-search'])
llm = OllamaLLM(model="qwen3:4b")  # Fixed model name

reminders = []

def setReminders(task: str) -> str:
    '''Sets a reminder for a given task'''
    reminders.append({'task': task, 'time': datetime.datetime.now()})
    return f'Reminder set for {task}.'

reminder_tool = Tool(
    name='Set reminder',
    func=setReminders,
    description='This tool is useful for creating reminders where the input should be the full description of the task.'
)

# Fix: Properly combine the tools - extend the search_tools list with reminder_tool
all_tools = search_tools + [reminder_tool]

agent = initialize_agent(
    tools=all_tools, 
    llm=llm, 
    agent='zero-shot-react-description', 
    verbose=True
)

# Example usage
response = agent.run("What is the current population of Canada? Also, remind me to check the weather in 2 hours.")
print(response)