import requests
from langchain.tools import BaseTool
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('API_KEY')

class WeatherTool(BaseTool):
    name = 'Weather'
    description = 'A tool to get the current weather conditions for a specified city'

    def _run(self, city: str) -> str:
        '''Fetches the current weather for the specified city using OpenWeatherMap API.'''

        try:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric'
            
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
        
    async def _arun(self, city: str) -> str:
        return 'Asynchronous weather fetching not implemented yet'
    
    