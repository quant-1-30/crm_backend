# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List
from sqlalchemy import select, and_
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Depends

from schema.operator import *
from schema.schema import *
from .home import get_current_user

router = APIRouter()

# broadcast
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)

manager = ConnectionManager()
@router.websocket("/ws/broadcast")
async def broadcast(websocket: WebSocket, user: User=Depends(get_current_user)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Broadcast: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/notify/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token, user: User=Depends(get_current_user)):
    if token != "secure_token":  # Example token validation
        await websocket.close(code=1008)  # Policy violation
        raise HTTPException(status_code=403, detail="Unauthorized")

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Client {client_id} says: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
 
@router.get("/api")
def api():
    return {"route": "ws"}
