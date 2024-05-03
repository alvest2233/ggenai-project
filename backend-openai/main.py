import asyncio
import websockets
import json
import os
import logging
from dotenv import load_dotenv
import openai

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

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
        await send_initial_response(room_id, message)

async def send_initial_response(room_id, message):
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": True, "id": room_id}))
    response = openai.Completion.create(
        engine="davinci",  # Choose an appropriate engine
        prompt=message,
        max_tokens=150
    )
    initial_response = response.choices[0].text.strip()
    await send_message(room_id, "server", initial_response)
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": False, "id": room_id}))

async def broadcast(room_id, message):
    for client in rooms[room_id]["clients"]:
        await client.send(message)

def main():
    start_server = websockets.serve(handle_client, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
