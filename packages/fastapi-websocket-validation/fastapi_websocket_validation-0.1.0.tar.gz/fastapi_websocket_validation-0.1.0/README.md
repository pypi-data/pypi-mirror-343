# WebSocket Validation

A Python library for handling and validating WebSocket messages in FastAPI applications with Pydantic models.

## Installation

```bash
pip install fastapi-websocket-validation
```

## Features

- Type-safe WebSocket message handling
- Automatic payload validation using Pydantic models
- Schema generation for WebSocket messages
- Easy-to-use decorator-based message registration

## Quick Start

```python
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from websocket_validation import WebSocketHandler, WebSocketMessage

app = FastAPI()
ws_handler = WebSocketHandler()

# Define your message payload models
class ChatMessage(BaseModel):
    message: str
    room_id: str

# Register a handler for chat messages
@ws_handler.register_handler("chat", ChatMessage)
async def handle_chat(websocket: WebSocket, payload: ChatMessage):
    await websocket.send_json({
        "type": "chat",
        "payload": {"message": f"Received: {payload.message}"}
    })

# Register the outgoing chat messages
ws_handler.register_outgoing_message_schema("chat", ChatMessage)

# Handle incoming messages
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        message = WebSocketMessage(**data)
        await ws_handler.dispatch(websocket, message)

# Get the schema for all message types
@app.get("/schema")
async def get_schema():
    return ws_handler.get_schema()
```

## Documentation

For more examples and detailed documentation, visit our [GitHub repository](https://github.com/yourusername/websocket-validation).

## License

This project is licensed under the MIT License - see the LICENSE file for details. 