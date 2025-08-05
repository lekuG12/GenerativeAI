from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


llm = HuggingFaceEndpoint(
    repo_id="gpt2",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="auto",  # let Hugging Face choose the best provider for you
)

chat_model = ChatHuggingFace(llm=llm)




# from langchain.schema import (
#     HumanMessage,
#     SystemMessage,
#     AIMessage,
# )


# messages = [
#     SystemMessage(content="You are a helpful assistant that answers questions about historical events."),
#     HumanMessage(content='Who is Marie Curie?')
# ]