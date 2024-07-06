from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import getpass
import os

os.environ["GROQ_API_KEY"] = "Groq_api_key"

from langchain_groq import ChatGroq

model = ChatGroq(model="llama3-8b-8192")
# Load tokenizer and model once
# tokenizer = AutoTokenizer.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.2-AWQ")
# model = AutoModelForCausalLM.from_pretrained("TheBloke/Mistral-7B-Instruct-v0.2-AWQ").cuda()  # Move model to GPU

# Define personality system messages
personalities = {
    "friendly": "You are a friendly assistant who uses casual and warm language.",
    "formal": "You are a formal assistant who uses professional and polite language.",
    "humorous": "You are a humorous assistant who uses jokes and playful language."
}

# Function to generate response based on personality
def generate_response(prompt, system_message):
    prompt_template = f"[INST] {system_message} {prompt} [/INST]"
    try:
        response = model.invoke(prompt_template)
        # Assuming response is an instance of AIMessage
        generated_text = response.content.strip()
        return generated_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, something went wrong while generating the response."

def main():
    print("Welcome! Please select a personality for the assistant:")
    print("1. Friendly")
    print("2. Formal")
    print("3. Humorous")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == "1":
        personality = "friendly"
    elif choice == "2":
        personality = "formal"
    elif choice == "3":
        personality = "humorous"
    else:
        print("Invalid choice. Defaulting to Friendly.")
        personality = "friendly"
    
    print(f"You have selected {personality} personality.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        system_message = personalities[personality]
        response = generate_response(user_input, system_message)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()
