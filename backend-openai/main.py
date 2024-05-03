import asyncio
import websockets
import json
import os
import logging
import httpx
from dotenv import load_dotenv

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

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
    rooms[room_id]["clients"].add(websocket)
    print(f"Room {room_id}: {room_name} ({len(rooms[room_id]['clients'])} clients)")
    await websocket.send(json.dumps({"route": "receive-room", "id": room_id, "name": room_name}))

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
    room_id = data.get("id")
    message = data.get("message")
    await send_message(room_id, "user", message)
    await handle_chat_message(room_id, message)

async def handle_chat_message(room_id, message):
    print(f"Room {room_id}: {message}")
    if rooms[room_id]["first_message"]:
        rooms[room_id]["first_message"] = False
        rooms[room_id]["original_prompt"] = message
    await send_initial_response(room_id, message)

async def send_initial_response(room_id, message):
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": True, "id": room_id}))
    response = await fetch_openai_response(message)
    await send_message(room_id, "server", response)
    await broadcast(room_id, json.dumps({"route": "chat-loading", "loading": False, "id": room_id}))

async def fetch_openai_response(prompt):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
        )
        response_data = response.json()
        return response_data['choices'][0]['message']['content']

async def broadcast(room_id, message):
    for client in rooms[room_id]["clients"]:
        await client.send(message)

def main():
    start_server = websockets.serve(handle_client, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
