import os
from dotenv import load_dotenv
from gemini import Gemini
from processes.extractors import extract_pages, extract_html

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
gemini_client = Gemini(api_key=os.environ.get("GEMINI_API_KEY"))

def main():
    # Ask the user what they want to make
    initial_prompt = input("What do you want to make today? ")

    # Get the initial response from the AI
    print("Getting Initial Response...")
    initial_response = gemini_client.request_initial_response(initial_prompt)
    print(initial_response)

    # Get the wireframe chain from the AI
    print("Getting Wireframe Chain...")
    screens = extract_pages(gemini_client.request_diagram(initial_prompt))

    # Check that the wireframe chain has exactly 3 screens
    if len(screens) != 3:
        raise Exception("The wireframe chain must have exactly 3 screens.")

    # Get the theme from the AI
    print("Getting Theme...")
    theme = gemini_client.request_theme(initial_prompt)

    # Generate the HTML for each screen and save it to test_output folder
    for i, screen in enumerate(screens, start=1):
        print(f"Generating HTML for Screen {i}...")
        screen_html = extract_html(gemini_client.request_generate_code(screen["prompt"], theme))
        with open(f"test_output/screen{i}.html", "w") as f:
            f.write(screen_html)

    print("DONE!")

def follow_up():
    followup_prompt = input("What do you want to make today? ")

    # Get type of message from the AI
    message_type = "GENERAL_INQUIRY"

if __name__ == "__main__":
    main()
    # follow_up()
