import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key loaded from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def request_initial_response(prompt: str):
    response = openai.Completion.create(
        engine="gpt-4",  # Switched to GPT-4 for enhanced capabilities
        prompt=prompt,
        max_tokens=1024,
        temperature=0,  # Zero temperature for deterministic output
        top_p=1.0,
        n=1
    )
    print("request_initial_response", response.choices[0].text)
    return response.choices[0].text

def request_diagram(prompt: str):
    response = openai.Completion.create(
        engine="gpt-4",  # Consistent use of GPT-4
        prompt=prompt,
        max_tokens=2048,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_diagram", response.choices[0].text)
    return response.choices[0].text

def request_theme(prompt: str):
    response = openai.Completion.create(
        engine="gpt-4",  # Using GPT-4 across all functions
        prompt=prompt,
        max_tokens=2048,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_theme", response.choices[0].text)
    return response.choices[0].text

def request_generate_code(prompt: str, theme: str):
    full_prompt = f"{prompt}\nTheme: {theme}"
    response = openai.Completion.create(
        engine="gpt-4",  # Using GPT-4, which is also suitable for code generation
        prompt=full_prompt,
        max_tokens=4096,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_generate_code", response.choices[0].text)
    return response.choices[0].text

def request_question_classification(prompt: str):
    response = openai.Completion.create(
        engine="gpt-4",  # Standardizing on GPT-4 for consistency
        prompt=prompt,
        max_tokens=512,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_question_classification", response.choices[0].text)
    return response.choices[0].text

def request_general_inquiry(prompt: str, original_prompt: str):
    combined_prompt = f"Question: {prompt}\nContext: {original_prompt}"
    response = openai.Completion.create(
        engine="gpt-4",  # GPT-4 to handle complex inquiries
        prompt=combined_prompt,
        max_tokens=1024,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_general_inquiry", response.choices[0].text)
    return response.choices[0].text

def request_code_change(prompt: str, html: str):
    full_prompt = f"Modify this HTML: {html}\n{prompt}"
    response = openai.Completion.create(
        engine="gpt-4",  # GPT-4 for handling HTML and code changes
        prompt=full_prompt,
        max_tokens=4096,
        temperature=0,
        top_p=1.0,
        n=1
    )
    print("request_code_change", response.choices[0].text)
    return response.choices[0].text
