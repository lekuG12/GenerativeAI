from langchain.tools import BaseTool
from typing import Type
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
import requests


load_dotenv()
token = os.getenv('GOOGLE')

class TextInput(BaseModel):
    text: str = Field(description='The text to be translated')

class TranslateTool(BaseTool):
    name: str = 'Translate'
    description: str = 'A tool to translate text from one language to another using google translate API'
    args_schema: Type[BaseModel] = TextInput

    def _run(self, text: str) -> str:
        try:
            url = 'https://translation.googleapis.com/language/translate/v2'
            params = {
                'q': text,
                'target': 'fr',  # Example target language
                'key': token
            }
        except Exception as e:
            return f"Error in translation: {str(e)}"
