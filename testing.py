from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
import dotenv
from huggingface_hub import login
import os

dotenv.load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if HUGGINGFACEHUB_API_TOKEN:
    login(token=HUGGINGFACEHUB_API_TOKEN)

hf = HuggingFacePipeline.from_model_id(
    model_id='gpt2',
    task='text-generation',
    pipeline_kwargs={'max_new_tokens': 100}
)

template = """Question: {question}
Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

chain = prompt | hf

question = 'Write a short story about a cat who goes on an adventure.'

print(chain.invoke({'question': question}))