import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key loaded from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Adjusted to the correct model name
            messages=[
                {"role": "user", "content": "generate html code for a startup"}
            ],
            max_tokens=4096,
            temperature=1,
            top_p=0.95
        )
        # Correctly access the 'message' key in the response
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['message']['content']
            print(message)
        else:
            print("No 'choices' found in the response or 'choices' is empty.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    generate()
