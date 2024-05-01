def extract_pages(input_string):
    screens = []

    # Find the start and end indices of the <screens> element
    start_index = input_string.find("<screens>")
    end_index = input_string.find("</screens>")

    if start_index != -1 and end_index != -1:
        # Extract the content inside the <screens> element
        screens_content = input_string[start_index + len("<screens>"):end_index].strip()

        # Split the content into individual <screen> elements
        screen_elements = screens_content.split("</screen>")

        for screen_element in screen_elements:
            # Extract the <name> and <prompt> values for each screen
            name_start = screen_element.find("<name>")
            name_end = screen_element.find("</name>")
            prompt_start = screen_element.find("<prompt>")
            prompt_end = screen_element.find("</prompt>")

            if name_start != -1 and name_end != -1 and prompt_start != -1 and prompt_end != -1:
                name = screen_element[name_start + len("<name>"):name_end].strip()
                prompt = screen_element[prompt_start + len("<prompt>"):prompt_end].strip()

                screens.append({"name": name, "prompt": prompt})

    return screens


def extract_ai_response(input_string):
    # Find the start and end indices of the <AI-RESPONSE> element
    start_index = input_string.find("<AI-RESPONSE>")
    end_index = input_string.find("</AI-RESPONSE>")

    if start_index != -1 and end_index != -1:
        # Extract the content inside the <AI-RESPONSE> element
        return input_string[start_index + len("<AI-RESPONSE>"):end_index].strip()

    return "Okay!"


def extract_html(input_string):
    # Find the start and end indices of the <html> element
    start_index = input_string.find("<html")
    end_index = input_string.find("</html>")

    if start_index != -1 and end_index != -1:
        return input_string[start_index:end_index + len("</html>")].strip()

    raise Exception("HTML Content Failed To Generate! This is possibly because Gemini refused to generate the HTML content.")
