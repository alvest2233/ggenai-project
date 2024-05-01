import vertexai
from vertexai.language_models import TextGenerationModel

def request_initial_response(client: TextGenerationModel, prompt: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=1024,
        top_p=1.0,
        top_k=40
    )
    print("request_initial_response", response.text)
    return response.text

def request_diagram(client: TextGenerationModel, prompt: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=2048,
        top_p=1.0,
        top_k=40
    )
    print("request_diagram", response.text)
    return response.text

def request_theme(client: TextGenerationModel, prompt: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=2048,
        top_p=1.0,
        top_k=40
    )
    print("request_theme", response.text)
    return response.text

def request_generate_code(client: TextGenerationModel, prompt: str, theme: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=4096,
        top_p=1.0,
        top_k=40
    )
    print("request_generate_code", response.text)
    return response.text

def request_question_classification(client: TextGenerationModel, prompt: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=512,
        top_p=1.0,
        top_k=40
    )
    print("request_question_classification", response.text)
    return response.text

def request_general_inquiry(client: TextGenerationModel, prompt: str, original_prompt: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=1024,
        top_p=1.0,
        top_k=40
    )
    print("request_general_inquiry", response.text)
    return response.text

def request_code_change(client: TextGenerationModel, prompt: str, html: str):
    response = client.predict(
        prompt,
        temperature=0,
        max_output_tokens=4096,
        top_p=1.0,
        top_k=40
    )
    print("request_code_change", response.text)
    return response.text

