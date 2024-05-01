import asyncio
import websockets
import json
from typing import cast
from dotenv import load_dotenv
from gemini.client import GeminiClient
import logging
import os

from processes.ai_tasks import (
    request_initial_response,
    request_diagram,
    request_theme,
    request_generate_code,
    request_question_classification,
    request_code_change,
    request_general_inquiry
)
from processes.extractors import extract_pages, extract_html, extract_ai_response

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.environ.get("GEMINI_API_KEY")
gemini_client = GeminiClient(api_key=gemini_api_key)

rooms = {}
recent_room = None


async def handle_client(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        route = data.get("route")

        if route == "join-room":
            await join_room(websocket, data)

        elif route == "leave-room":
            await leave_room(websocket, data)

        elif route == "chat-user":
            await chat_user(websocket, data)

        elif route == "recent":
            await websocket.send(json.dumps({"route": "recent", "id": recent_room}))

        else:
            await websocket.send(json.dumps({"route": "error", "message": "Invalid route"}))


async def join_room(websocket, data):
    room_id = data.get("id")
    room_name = data.get("name", "New Room")
    if room_id not in rooms:
        rooms[room_id] = {
            "name": room_name,
            "clients": set(),
            "messages": list(),
            "diagram": None,
            "pages": dict(),
            "first_message": True,
            "original_prompt": ""
        }
        global recent_room
        recent_room = room_id
    for c in list(rooms[room_id]["clients"]):
        if not c.open:
            rooms[room_id]["clients"].remove(c)
    rooms[room_id]["clients"].add(websocket)
    print(f"Room {room_id}: {room_name} ({len(rooms[room_id]['clients'])} clients)")
    await websocket.send(json.dumps({"route": "receive-room", "id": room_id, "name": room_name}))
    for (m_author, m_content) in rooms[room_id]["messages"]:
        if m_author == "server":
            await websocket.send(json.dumps({"route": "chat-server", "message": m_content, "id": room_id}))
        elif m_author == "user":
            await websocket.send(json.dumps({"route": "chat-user", "message": m_content, "id": room_id}))
        else:
            raise ValueError("Invalid message author")
    if rooms[room_id]["diagram"]:
        await websocket.send(json.dumps({"route": "diagram", "diagram": rooms[room_id]["diagram"], "id": room_id}))
    for page_id, page_content in rooms[room_id]["pages"].items():
        await websocket.send(json.dumps({"route": "receive-page", "page": {"id": page_id, "html": page_content}, "id": room_id}))


async def send_message(room_id, author, message):
    if author not in ("server", "user"):
        raise ValueError("Invalid message author")
    rooms[room_id]["messages"].append((author, message))
    await broadcast(room_id, json.dumps({"route": f"chat-{author}", "message": message, "id": room_id}))


async def leave_room(websocket, data):
    room_id = data.get("id")
    rooms[room_id]["clients"].remove(websocket)
    print(f"Room {room_id}: {rooms[room_id]['name']} ({len(rooms[room_id]['clients'])} clients)")
    await websocket.send(json.dumps({"route": "leave-room"}))


async def chat_user(websocket, data):
    try:
        room_id = data.get("id")
        message = data.get("message")

        await send_message(room_id, "user", message)
        await handle_chat_message(room_id, message)
    except Exception as e:
        await send_message(room_id, "server", f"An error occurred: {str(e)}")
        await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": False, "id": room_id}))
        await broadcast(room_id, json.dumps({"route": "diagram-loading", "loading": False, "id": room_id}))


async def handle_chat_message(room_id, message):
    print(f"Room {room_id}: {message}")
    if rooms[room_id]["first_message"]:
        rooms[room_id]["first_message"] = False
        rooms[room_id]["original_prompt"] = message
        # First message!
        await asyncio.gather(
            send_initial_response(room_id, message),
            send_diagram(room_id, message)
        )
    else:
        await handle_followup_message(room_id, message)


async def send_initial_response(room_id, message):
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": True, "id": room_id}))
    initial_response = gemini_client.request_initial_response(message)
    await send_message(room_id, "server", initial_response)
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": False, "id": room_id}))


async def send_diagram(room_id, message):
    await broadcast(room_id, json.dumps({"route": "diagram-loading", "loading": True, "id": room_id}))
    diagram_xml, theme = gemini_client.request_diagram(message)

    diagram_pages = extract_pages(diagram_xml)
    if len(diagram_pages) != 3:
        raise ValueError("The diagram chain must have exactly 3 pages.")

    rooms[room_id]["diagram"] = [diagram_pages[0]["name"], diagram_pages[1]["name"], diagram_pages[2]["name"]]
    await broadcast(room_id, json.dumps({"route": "diagram", "diagram": rooms[room_id]["diagram"], "id": room_id}))

    await asyncio.gather(
        generate_and_send_page(room_id, diagram_pages[0]["name"], diagram_pages[0]["prompt"], theme),
        generate_and_send_page(room_id, diagram_pages[1]["name"], diagram_pages[1]["prompt"], theme),
        generate_and_send_page(room_id, diagram_pages[2]["name"], diagram_pages[2]["prompt"], theme)
    )
    await broadcast(room_id, json.dumps({"route": "diagram-loading", "loading": False, "id": room_id}))


async def generate_and_send_page(room_id, page_id, prompt, theme):
    code_response = gemini_client.request_generate_code(prompt, theme)
    html = extract_html(code_response)
    rooms[room_id]["pages"][page_id] = html
    await broadcast(room_id, json.dumps({"route": "receive-page", "page": {"id": page_id, "html": html}, "id": room_id}))


async def handle_followup_message(room_id, message):
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": True, "id": room_id}))

    message_category = gemini_client.request_question_classification(message)
    if "CODE_CHANGE" in message_category:
        await handle_code_change(room_id, message)
    else:
        await handle_general_inquiry(room_id, message)

    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": False, "id": room_id}))


async def handle_code_change(room_id, message):
    await broadcast(room_id, json.dumps({"route": "diagram-loading", "loading": True, "id": room_id}))
    tasks = []
    for page_id, page_content in rooms[room_id]["pages"].items():
        tasks.append(handle_single_code_change(room_id, message, page_id, page_content))

    response = list(await asyncio.gather(*tasks))[0]
    await broadcast(room_id, json.dumps({"route": "diagram-loading", "loading": False, "id": room_id}))
    await send_message(room_id, "server", response)


async def handle_single_code_change(room_id, message, page_id, page_content):
    code_response = gemini_client.request_code_change(message, page_content)
    html = extract_html(code_response)
    text = extract_ai_response(code_response)
    rooms[room_id]["pages"][page_id] = html
    await broadcast(room_id, json.dumps({"route": "receive-page", "page": {"id": page_id, "html": html}, "id": room_id}))
    return text


async def handle_general_inquiry(room_id, message):
    response = gemini_client.request_general_inquiry(message, rooms[room_id]["original_prompt"])
    await send_message(room_id, "server", response)


async def broadcast(room_id, message):
    for client in rooms[room_id]["clients"]:
        await client.send(message)


def main():
    start_server = websockets.serve(handle_client, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
