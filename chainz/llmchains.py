from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate

llm = HuggingFacePipeline.from_model_id(
    model_id="gpt2",
    task="text-generation",
    pipeline_kwargs=dict(
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        temperature=0.7,
    ),
)

template = """Question: {input}
Answer: Let's think step by step."""

prompt = PromptTemplate(template=template)

chain = prompt | llm

input_text = 'Who is Marie Curie?'
response = chain.invoke({'input':input_text})

print(f"Response: {response}")