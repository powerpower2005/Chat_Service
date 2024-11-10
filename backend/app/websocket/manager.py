from fastapi import WebSocket
from typing import Dict, List, Set

# Class for managing connected clients
class ConnectionManager:
    def __init__(self):
        # Dictionary to store active connections by room
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        """Connect a client to a specific room"""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, room_id: str):
        """Disconnect a client from a room"""
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:
            del self.active_connections[room_id]
    
    async def broadcast(self, message: str, room_id: str):
        """Broadcast message to all clients in a room"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)
    
    def get_clients_count(self, room_id: str) -> int:
        """Return the number of connected clients in a specific room"""
        return len(self.active_connections.get(room_id, set()))

