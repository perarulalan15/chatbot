import chainlit as cl
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os

os.environ["GROQ_API_KEY"] = "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"

from langchain_groq import ChatGroq

# Initialize the model
model = ChatGroq(model="llama3-8b-8192")

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
        generated_text = response.content.strip()
        return generated_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, something went wrong while generating the response."

# Keep track of selected personality and first message flag
selected_personality = "friendly"
first_message = True

@cl.on_message
async def main(message: cl.Message):
    global selected_personality, first_message

    user_input = message.content.strip().lower()

    if first_message:
        first_message = False
        await cl.Message(
            content="Welcome! Please select a personality for the assistant:\n1. Friendly\n2. Formal\n3. Humorous"
        ).send()
        return

    if user_input in ["1", "2", "3"]:
        if user_input == "1":
            selected_personality = "friendly"
        elif user_input == "2":
            selected_personality = "formal"
        elif user_input == "3":
            selected_personality = "humorous"

        await cl.Message(
            content=f"You have selected {selected_personality} personality."
        ).send()
    else:
        system_message = personalities[selected_personality]
        response = generate_response(user_input, system_message)

        await cl.Message(
            content=response
        ).send()
