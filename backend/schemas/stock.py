"""
Pydantic schemas for stock data
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class StockSymbol(BaseModel):
    """Stock symbol information"""
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL)")
    name: str = Field(..., description="Company name")
    exchange: str = Field(..., description="Stock exchange")

class StockData(BaseModel):
    """Individual stock data point"""
    time: datetime = Field(..., description="Timestamp of the data point")
    symbol: str = Field(..., description="Stock symbol")
    open: float = Field(..., description="Opening price")
    high: float = Field(..., description="Highest price")
    low: float = Field(..., description="Lowest price")
    close: float = Field(..., description="Closing price")
    volume: int = Field(..., description="Trading volume")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }

class StockDataResponse(BaseModel):
    """Response model for stock data queries"""
    symbol: str = Field(..., description="Stock symbol")
    interval: str = Field(..., description="Data interval")
    start_time: datetime = Field(..., description="Start time of data range")
    end_time: datetime = Field(..., description="End time of data range")
    data: List[StockData] = Field(..., description="List of stock data points")
    count: int = Field(..., description="Number of data points returned")

class StockStatistics(BaseModel):
    """Statistical information about a stock"""
    symbol: str
    current_price: Optional[float] = None
    price_change: Optional[float] = None
    price_change_percent: Optional[float] = None
    volume_avg_30d: Optional[float] = None
    volatility: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    market_cap: Optional[float] = None

class OHLCData(BaseModel):
    """OHLC data point for charting"""
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockIngestionRequest(BaseModel):
    """Request model for stock data ingestion"""
    symbol: str = Field(..., description="Stock symbol to ingest")
    source: str = Field(default="yahoo", description="Data source (yahoo, polygon, eodhd)")
    start_date: Optional[datetime] = Field(None, description="Start date for historical data")
    end_date: Optional[datetime] = Field(None, description="End date for historical data")

class StockIngestionResponse(BaseModel):
    """Response model for stock data ingestion"""
    symbol: str
    status: str
    records_processed: int
    start_time: datetime
    end_time: datetime
    message: Optional[str] = None