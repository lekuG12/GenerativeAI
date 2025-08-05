from getpass import getpass
import dotenv 
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

dotenv.load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

question = "What is the capital of France?"
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

repo_id = "microsoft/DialoGPT-medium"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
)

llm_chain = prompt | llm
print(llm_chain.invoke({"question": question}))