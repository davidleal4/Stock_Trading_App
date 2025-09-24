"""
FastAPI backend for Stock Trading Application
Provides APIs for data ingestion, ML models, and trading functionality
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging
from typing import List

from core.config import settings
from core.database import init_db
from api.routes import stocks, models, trading, agent
from core.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize WebSocket manager
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Stock Trading Application")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Stock Trading Application")

# Create FastAPI app
app = FastAPI(
    title="Stock Trading Application API",
    description="ML-powered stock trading platform with real-time data and AI assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API routes
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(trading.router, prefix="/api/trading", tags=["trading"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Stock Trading Application API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back for now - implement specific handlers later
            await websocket_manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

@app.websocket("/ws/stocks/{symbol}")
async def stock_websocket(websocket: WebSocket, symbol: str):
    """WebSocket endpoint for real-time stock data"""
    await websocket_manager.connect(websocket)
    try:
        # Send initial connection confirmation
        await websocket_manager.send_personal_message(
            f"Connected to {symbol} real-time data", websocket
        )
        
        # Keep connection alive - real-time data will be pushed by background tasks
        while True:
            await asyncio.sleep(1)
            # Placeholder for real-time data streaming
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )