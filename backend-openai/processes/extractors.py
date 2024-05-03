import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def extract_pages(input_string):
    screens = []
    try:
        # Parsing the input string as XML
        root = ET.fromstring(f"<data>{input_string}</data>")  # Wrap with a root tag to ensure proper parsing
        for screen in root.findall('.//screen'):
            name = screen.find('name').text.strip() if screen.find('name') is not None else "Unnamed"
            prompt = screen.find('prompt').text.strip() if screen.find('prompt') is not None else "No prompt"
            screens.append({"name": name, "prompt": prompt})
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    return screens

def extract_ai_response(input_string):
    try:
        root = ET.fromstring(f"<data>{input_string}</data>")  # Wrap with a root tag
        ai_response = root.find('.//AI-RESPONSE')
        return ai_response.text.strip() if ai_response is not None else "No AI response found"
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return "No AI response found"

def extract_html(input_string):
    try:
        soup = BeautifulSoup(input_string, 'html.parser')
        html_content = soup.find('html')
        if html_content:
            return str(html_content)
        else:
            raise ValueError("HTML content not found")
    except Exception as e:
        raise Exception(f"Failed to extract HTML: {str(e)}")

