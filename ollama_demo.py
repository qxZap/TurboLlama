from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

conversation_memory = []

ollama = Ollama(base_url="http://localhost:11434", model="mistral")

def chat_with_ollama(prompt):
    response = ollama(prompt)
    return response

def update_memory(question, answer):
    conversation_memory.append(f"Question: {question}\nAnswer: {answer}")
    if len(conversation_memory) > 10:
        conversation_memory.pop(0)

template = """
Question: {question}

Answer:
"""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=ollama)

print("Chatbot initialized, ready to chat...")
while True:
    question = input("> ")
    contextual_prompt = "\n".join(conversation_memory) + f"\nQuestion: {question}\n"
    answer = llm_chain.run(contextual_prompt)
    update_memory(question, answer)
    print(answer, '\n')
