from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="llama3",  
    temperature=0  
)

system_prompt = """
You are a polite hotel receptionist.

Your job:
1. Collect all necessary booking information from the user:
   - guest_name
   - room_type
   - check_in
   - check_out
   - num_guests
2. Ask only one question at a time if a field is missing.
3. If the user gives information implicitly, infer it naturally.
4. Do not show internal notes or reasoning.
5. When all fields are available, return **only valid JSON** in this format:

{{
  "guest_name": string or null,
  "room_type": string or null,
  "check_in": string or null,
  "check_out": string or null,
  "num_guests": integer or null
}}

6. Speak naturally and politely. Do not repeat JSON or explain it.
7. If the user wants to end the conversation ("bye", "exit", "quit"), politely finish the chat without returning JSON.

"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{conversation}")
])

chain = prompt | llm

conversation = ""
print("Receptionist: Welcome to our hotel! How may I help you today?")

while True:
    user_input = input("User: ")

   
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nReceptionist: Thank you for contacting us. Have a great day!")
        break

    conversation += f"\nUser: {user_input}"

    
    response = chain.invoke({"conversation": conversation})
    answer = response.content.strip()

    print("\nReceptionist:", answer)
    conversation += f"\nReceptionist: {answer}"

    if answer.startswith("{") and answer.endswith("}"):
        print("\nReceptionist: Your booking has been completed. Type 'exit' to close the chat.")
