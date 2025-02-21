from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOllama(model="mistral", base_url="http://localhost:11434")

# Define the prompt template for the chat
prompt = ChatPromptTemplate.from_messages([
    ("system", "be sarcastic at all times"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# Initialize the memory to store the chat history
memory = ConversationBufferMemory(return_messages=True)

# Create an LLMChain that combines the language model, prompt, and memory
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

# Simple loop to handle user input and generate responses
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chain.invoke({"input": user_input})
    print("Bot:", response["text"])
