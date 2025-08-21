from langchain_ollama.llms import OllamaLLM

llm = OllamaLLM(model="qwen3:4b")
response = llm.invoke("Explain quantum computing in simple terms.")
print(response)
