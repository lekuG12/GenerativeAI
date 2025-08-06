from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.prompts import PromptTemplate

llm = HuggingFacePipeline.from_model_id(
    model_id="facebook/blenderbot-400M-distill",
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