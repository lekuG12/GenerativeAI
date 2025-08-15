from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
hugging_keys = os.getenv("HUGGING_FACE_TOKEN")

prompts = PromptTemplate.from_template('Tell me a joke about {topic}')

llm = HuggingFaceHub(
    repo_id = "google/flan-t5-xl",
    model_kwargs = {'temperature': 0.9},
    huggingfacehub_api_token=hugging_keys
)

chain = prompts | llm

joke = chain.invoke({"topic": "cats"})
print(joke)