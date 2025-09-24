"""
Stock data API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio

from core.database import db_manager
from core.config import settings
from schemas.stock import StockData, StockDataResponse, StockSymbol
from services.stock_service import StockService

router = APIRouter()
stock_service = StockService()

@router.get("/symbols", response_model=List[StockSymbol])
async def get_available_symbols():
    """Get list of available stock symbols"""
    symbols = []
    for symbol in settings.DEFAULT_SYMBOLS:
        symbols.append(StockSymbol(
            symbol=symbol,
            name=f"{symbol} Corporation",  # Placeholder - would fetch from API
            exchange="NASDAQ"
        ))
    return symbols

@router.get("/{symbol}/data", response_model=StockDataResponse)
async def get_stock_data(
    symbol: str,
    start_time: Optional[datetime] = Query(None, description="Start time for data range"),
    end_time: Optional[datetime] = Query(None, description="End time for data range"),
    interval: str = Query("1m", description="Data interval (1m, 5m, 1h, 1d)"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum number of records")
):
    """Get historical stock data for a symbol"""
    
    # Default to last 24 hours if no time range specified
    if not end_time:
        end_time = datetime.utcnow()
    if not start_time:
        start_time = end_time - timedelta(hours=24)
    
    try:
        data = await stock_service.get_stock_data(
            symbol=symbol.upper(),
            start_time=start_time,
            end_time=end_time,
            interval=interval,
            limit=limit
        )
        
        return StockDataResponse(
            symbol=symbol.upper(),
            interval=interval,
            start_time=start_time,
            end_time=end_time,
            data=data,
            count=len(data)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")

@router.get("/{symbol}/latest")
async def get_latest_stock_data(symbol: str):
    """Get latest stock data for a symbol"""
    try:
        latest_data = await stock_service.get_latest_stock_data(symbol.upper())
        if not latest_data:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        return latest_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest data: {str(e)}")

@router.post("/{symbol}/ingest")
async def trigger_data_ingestion(symbol: str):
    """Trigger data ingestion for a specific symbol"""
    try:
        # This would typically trigger a background job
        await stock_service.ingest_stock_data(symbol.upper())
        return {"message": f"Data ingestion triggered for {symbol}", "status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering ingestion: {str(e)}")

@router.post("/ingest/all")
async def trigger_all_ingestion():
    """Trigger data ingestion for all default symbols"""
    try:
        results = []
        for symbol in settings.DEFAULT_SYMBOLS:
            try:
                await stock_service.ingest_stock_data(symbol)
                results.append({"symbol": symbol, "status": "success"})
            except Exception as e:
                results.append({"symbol": symbol, "status": "error", "error": str(e)})
        
        return {"message": "Data ingestion triggered for all symbols", "results": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering bulk ingestion: {str(e)}")

@router.get("/{symbol}/stats")
async def get_stock_statistics(symbol: str):
    """Get statistical information about a stock"""
    try:
        stats = await stock_service.get_stock_statistics(symbol.upper())
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@router.get("/{symbol}/ohlc")
async def get_ohlc_data(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="Number of days of OHLC data")
):
    """Get OHLC (Open, High, Low, Close) data for charting"""
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        ohlc_data = await stock_service.get_ohlc_data(
            symbol=symbol.upper(),
            start_time=start_time,
            end_time=end_time
        )
        
        return {
            "symbol": symbol.upper(),
            "period": f"{days} days",
            "data": ohlc_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching OHLC data: {str(e)}")