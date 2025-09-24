"""
WebSocket connection manager for real-time data streaming
"""

from fastapi import WebSocket
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections for real-time data streaming"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.stock_subscriptions: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # Remove from stock subscriptions
        for symbol, connections in self.stock_subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)
        
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")
            self.disconnect(websocket)
    
    async def send_json_to_connection(self, data: Dict[Any, Any], websocket: WebSocket):
        """Send JSON data to specific WebSocket connection"""
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.error(f"Error sending JSON to WebSocket: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast message to all active connections"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def broadcast_json(self, data: Dict[Any, Any]):
        """Broadcast JSON data to all active connections"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting JSON to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    def subscribe_to_stock(self, symbol: str, websocket: WebSocket):
        """Subscribe WebSocket to stock updates"""
        if symbol not in self.stock_subscriptions:
            self.stock_subscriptions[symbol] = []
        
        if websocket not in self.stock_subscriptions[symbol]:
            self.stock_subscriptions[symbol].append(websocket)
            logger.info(f"WebSocket subscribed to {symbol}")
    
    def unsubscribe_from_stock(self, symbol: str, websocket: WebSocket):
        """Unsubscribe WebSocket from stock updates"""
        if symbol in self.stock_subscriptions and websocket in self.stock_subscriptions[symbol]:
            self.stock_subscriptions[symbol].remove(websocket)
            logger.info(f"WebSocket unsubscribed from {symbol}")
    
    async def broadcast_stock_update(self, symbol: str, data: Dict[Any, Any]):
        """Broadcast stock data to subscribed connections"""
        if symbol not in self.stock_subscriptions:
            return
        
        disconnected = []
        for connection in self.stock_subscriptions[symbol]:
            try:
                await connection.send_json({
                    "type": "stock_update",
                    "symbol": symbol,
                    "data": data
                })
            except Exception as e:
                logger.error(f"Error sending stock update to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.unsubscribe_from_stock(symbol, connection)
            self.disconnect(connection)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def get_stock_subscriber_count(self, symbol: str) -> int:
        """Get number of subscribers for a specific stock"""
        return len(self.stock_subscriptions.get(symbol, []))