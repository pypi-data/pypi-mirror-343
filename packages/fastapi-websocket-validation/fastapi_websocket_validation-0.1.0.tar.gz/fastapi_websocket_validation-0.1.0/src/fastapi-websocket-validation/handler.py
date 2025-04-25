from fastapi import WebSocket
from typing import Dict, Any, Callable
from pydantic import BaseModel

class WebSocketMessage(BaseModel):
    """Base message schema for WebSocket messages."""
    type: str
    payload: Dict[str, Any]

class WebSocketHandler:
    """
    A handler class for managing WebSocket message types and their validation.
    
    This class provides functionality to:
    - Register message handlers with their corresponding Pydantic models
    - Validate incoming messages against their schemas
    - Dispatch messages to appropriate handlers
    - Generate documentation for the WebSocket messages
    """
    
    def __init__(self):
        self.handlers: Dict[str, tuple[Callable, BaseModel]] = {}
        self.incoming_message_schemas: Dict[str, Any] = {}
        self.outgoing_message_schemas: Dict[str, Any] = {}
    
    def register_handler(self, message_type: str, payload_model: type[BaseModel]):
        """
        Decorator to register handlers with their payload validation models.
        
        Args:
            message_type: The type identifier for the message
            payload_model: A Pydantic model class for validating the message payload
        """
        def decorator(func: Callable):
            self.handlers[message_type] = (func, payload_model)
            self.incoming_message_schemas[message_type] = payload_model
            return func
        return decorator

    def register_outgoing_message_schema(self, message_type: str, payload_model: type[BaseModel]):
        """
        Register outgoing message schema for documentation purposes.
        
        Args:
            message_type: The type identifier for the outgoing message
            payload_model: A Pydantic model class for the outgoing message payload
        """
        self.outgoing_message_schemas[message_type] = payload_model

    async def dispatch(self, websocket: WebSocket, message: WebSocketMessage):
        """
        Dispatch incoming message to appropriate handler.
        
        Args:
            websocket: The WebSocket connection instance
            message: The incoming WebSocket message
        """
        if message.type not in self.handlers:
            await websocket.send_json({
                "type": "error",
                "payload": {"message": f"Unknown message type: {message.type}"}
            })
            return
            
        handler, payload_model = self.handlers[message.type]
        try:
            # Validate payload against the model
            validated_payload = payload_model(**message.payload)
            # Call handler with validated payload
            await handler(websocket, validated_payload)
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "payload": {"message": str(e)}
            })

    def get_schema(self):
        """
        Get the schema for all message types.
        
        Returns:
            dict: A dictionary containing the schema for all registered message types
        """
        from pydantic import TypeAdapter
        
        # Collect all models and their documentation
        components = {}
        message_types = {}
        
        # Handle incoming messages
        for msg_type, (handler, request_model) in self.handlers.items():
            # Get request schema
            request_schema = TypeAdapter(request_model).json_schema()
            request_schema.pop('$defs', None)
            components[request_model.__name__] = request_schema
            
            # Document the message type
            message_types[msg_type] = {
                "description": handler.__doc__ or "No description available",
                "request": {
                    "payload_schema": request_model.__name__
                }
            }
            
        # Document outgoing messages
        for msg_type, model in self.outgoing_message_schemas.items():
            if model.__name__ not in components:
                schema = TypeAdapter(model).json_schema()
                schema.pop('$defs', None)
                components[model.__name__] = schema
            
            message_types[msg_type] = {
                "description": "Server message",
                "response": {
                    "payload_schema": model.__name__
                }
            }
            
        return {
            "info": {
                "title": "WebSocket API Schema",
                "version": "1.0.0",
                "description": "Schema for WebSocket messages"
            },
            "message_types": message_types,
            "components": {
                "schemas": components
            }
        } 