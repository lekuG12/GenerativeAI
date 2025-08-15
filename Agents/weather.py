import requests
from langchain.tools import BaseTool
from dotenv import load_dotenv
from typing import Optional, Type
import os
from pydantic import Field, BaseModel

load_dotenv()
token = os.getenv('API_KEY')

class WeatherInput(BaseModel):
    city: str = Field(description="The name of the city to get the weather for.")

class WeatherTool(BaseTool):
    name: str = 'Weather'
    description: str= 'A tool to get the current weather conditions for a specified city'
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, city: str) -> str:
        '''Fetches the current weather for the specified city using OpenWeatherMap API.'''

        try:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={token}&units=metric'
            
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()

            if 'list' in data and len(data['list']) > 0:
                current_weather = data['list'][0]
                city_name = data['city']['name']
                temperature = current_weather['main']['temp']
                weather_description = current_weather['weather'][0]['description']

            weather_info = f"""Weather in {city_name}\n\nTemperature: {temperature}°C\n\nCondition: {weather_description}"""
            return weather_info

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"
        
    async def _arun(self, city: str) -> str:
        return 'Asynchronous weather fetching not implemented yet'
    


if __name__ == '__main__':
    weather_tool = WeatherTool()
    print(weather_tool._run('Buea'))