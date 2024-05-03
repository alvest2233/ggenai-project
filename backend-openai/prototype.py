import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key loaded from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_html_screens(initial_response):
    """Generate and save HTML for three screens based on an initial response."""
    for i in range(1, 4):  # Assuming we want three screens
        screen_prompt = f"Generate HTML for screen {i} based on this description: {initial_response}"
        screen_response = openai.Completion.create(
            engine="gpt-4",  # Using GPT-4 for advanced capabilities
            prompt=screen_prompt,
            max_tokens=250,
            temperature=0.7  # Adjust temperature for creative but realistic responses
        )
        screen_html = screen_response.choices[0].text.strip()
        # Save the generated HTML to a file
        os.makedirs('test_output', exist_ok=True)  # Ensure the directory exists
        with open(f"test_output/screen{i}.html", "w") as f:
            f.write(screen_html)
        print(f"HTML for Screen {i} generated and saved.")

def main():
    # Get a user input for what they want to make
    initial_prompt = input("What do you want to make today? ")

    # Fetch an initial response from OpenAI based on the user's input
    print("Getting Initial Response...")
    initial_response = openai.Completion.create(
        engine="gpt-4",  # Using GPT-4 for initial response generation
        prompt=initial_prompt,
        max_tokens=150,
        temperature=0.7  # A moderate temperature for coherent and useful output
    )
    response_text = initial_response.choices[0].text.strip()
    print("Response:", response_text)

    # Generate HTML for the screens
    print("Generating HTML for screens based on the AI's response...")
    generate_html_screens(response_text)

    print("DONE! Check the 'test_output' directory for the generated HTML files.")

if __name__ == "__main__":
    main()
