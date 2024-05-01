from gemini import Gemini

def request_initial_response(client: Gemini, prompt: str):
    message = client.messages.create(
        model="your-gemini-model-for-initial-response",
        max_tokens=1024,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_initial_response", message.content[0].text)
    return message.content[0].text

def request_diagram(client: Gemini, prompt: str):
    message = client.messages.create(
        model="your-gemini-model-for-diagram",
        max_tokens=2048,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_diagram", message.content[0].text)
    return message.content[0].text

def request_theme(client: Gemini, prompt: str):
    message = client.messages.create(
        model="your-gemini-model-for-theme",
        max_tokens=2048,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_theme", message.content[0].text)
    return message.content[0].text

def request_generate_code(client: Gemini, prompt: str, theme: str):
    message = client.messages.create(
        model="your-gemini-model-for-generate-code",
        max_tokens=4096,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_generate_code", message.content[0].text)
    return message.content[0].text

def request_question_classification(client: Gemini, prompt: str):
    message = client.messages.create(
        model="your-gemini-model-for-question-classification",
        max_tokens=512,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_question_classification", message.content[0].text)
    return message.content[0].text

def request_general_inquiry(client: Gemini, prompt: str, original_prompt: str):
    message = client.messages.create(
        model="your-gemini-model-for-general-inquiry",
        max_tokens=1024,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_general_inquiry", message.content[0].text)
    return message.content[0].text

def request_code_change(client: Gemini, prompt: str, html: str):
    message = client.messages.create(
        model="your-gemini-model-for-code-change",
        max_tokens=4096,
        temperature=0,
        system="Your system prompt here...",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print("request_code_change", message.content[0].text)
    return message.content[0].text
