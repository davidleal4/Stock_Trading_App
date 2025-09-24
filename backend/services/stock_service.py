"""
Stock data service for fetching and managing stock information
"""

import asyncio
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd
import logging

from core.database import db_manager
from schemas.stock import StockData, StockStatistics, OHLCData

logger = logging.getLogger(__name__)

class StockService:
    """Service for managing stock data operations"""
    
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
    
    async def get_stock_data(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        interval: str = "1m",
        limit: int = 1000
    ) -> List[StockData]:
        """Fetch stock data from database"""
        
        # Map interval to appropriate query
        interval_mapping = {
            "1m": "1 minute",
            "5m": "5 minutes", 
            "15m": "15 minutes",
            "1h": "1 hour",
            "1d": "1 day"
        }
        
        # For demo purposes, generate some sample data if database is empty
        try:
            query = """
                SELECT time, symbol, open, high, low, close, volume
                FROM stock_data 
                WHERE symbol = $1 
                AND time >= $2 
                AND time <= $3
                ORDER BY time DESC
                LIMIT $4
            """
            
            if db_manager.pool:
                rows = await db_manager.fetch_many(query, symbol, start_time, end_time, limit)
                
                if not rows:
                    # Generate sample data for demo
                    return await self._generate_sample_data(symbol, start_time, end_time)
                
                return [
                    StockData(
                        time=row['time'],
                        symbol=row['symbol'],
                        open=float(row['open']),
                        high=float(row['high']),
                        low=float(row['low']),
                        close=float(row['close']),
                        volume=row['volume']
                    )
                    for row in rows
                ]
            else:
                # Fallback to sample data
                return await self._generate_sample_data(symbol, start_time, end_time)
                
        except Exception as e:
            logger.error(f"Error fetching stock data: {e}")
            # Return sample data as fallback
            return await self._generate_sample_data(symbol, start_time, end_time)
    
    async def _generate_sample_data(
        self, 
        symbol: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[StockData]:
        """Generate sample stock data for demo purposes"""
        
        base_prices = {
            "AAPL": 150.0,
            "MSFT": 300.0,
            "NVDA": 400.0,
            "GOOG": 2500.0,
            "AMZN": 130.0,
            "META": 280.0,
            "TSLA": 250.0,
            "BRK.B": 350.0,
            "JPM": 140.0,
            "V": 220.0
        }
        
        base_price = base_prices.get(symbol, 100.0)
        data_points = []
        
        # Generate hourly data points
        current_time = start_time
        current_price = base_price
        
        while current_time <= end_time:
            # Simple random walk for demo
            import random
            change_percent = random.uniform(-0.02, 0.02)  # ±2% change
            price_change = current_price * change_percent
            
            open_price = current_price
            close_price = current_price + price_change
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.01))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.01))
            volume = random.randint(100000, 2000000)
            
            data_points.append(StockData(
                time=current_time,
                symbol=symbol,
                open=round(open_price, 2),
                high=round(high_price, 2),
                low=round(low_price, 2),
                close=round(close_price, 2),
                volume=volume
            ))
            
            current_price = close_price
            current_time += timedelta(hours=1)
        
        return data_points[-100:]  # Return last 100 points
    
    async def get_latest_stock_data(self, symbol: str) -> Optional[StockData]:
        """Get the most recent stock data for a symbol"""
        try:
            query = """
                SELECT time, symbol, open, high, low, close, volume
                FROM stock_data 
                WHERE symbol = $1 
                ORDER BY time DESC
                LIMIT 1
            """
            
            if db_manager.pool:
                row = await db_manager.fetch_one(query, symbol)
                
                if row:
                    return StockData(
                        time=row['time'],
                        symbol=row['symbol'],
                        open=float(row['open']),
                        high=float(row['high']),
                        low=float(row['low']),
                        close=float(row['close']),
                        volume=row['volume']
                    )
            
            # Fallback to generating single sample data point
            sample_data = await self._generate_sample_data(
                symbol, 
                datetime.utcnow() - timedelta(hours=1),
                datetime.utcnow()
            )
            return sample_data[0] if sample_data else None
            
        except Exception as e:
            logger.error(f"Error fetching latest stock data: {e}")
            return None
    
    async def ingest_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Ingest stock data from external source"""
        try:
            # For demo, we'll use yfinance to get real data
            ticker = yf.Ticker(symbol)
            
            # Get last 5 days of minute data
            hist = ticker.history(period="5d", interval="1m")
            
            if hist.empty:
                return {"status": "error", "message": "No data available"}
            
            # Insert data into database
            records_inserted = 0
            if db_manager.pool:
                insert_query = """
                    INSERT INTO stock_data (time, symbol, open, high, low, close, volume)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (time, symbol) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                """
                
                for timestamp, row in hist.iterrows():
                    try:
                        await db_manager.execute(
                            insert_query,
                            timestamp.to_pydatetime(),
                            symbol,
                            float(row['Open']),
                            float(row['High']),
                            float(row['Low']),
                            float(row['Close']),
                            int(row['Volume'])
                        )
                        records_inserted += 1
                    except Exception as e:
                        logger.warning(f"Failed to insert record for {symbol}: {e}")
            
            return {
                "status": "success",
                "records_inserted": records_inserted,
                "message": f"Ingested {records_inserted} records for {symbol}"
            }
            
        except Exception as e:
            logger.error(f"Error ingesting data for {symbol}: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_stock_statistics(self, symbol: str) -> StockStatistics:
        """Get statistical information about a stock"""
        try:
            # For demo, return sample statistics
            latest_data = await self.get_latest_stock_data(symbol)
            
            if not latest_data:
                return StockStatistics(symbol=symbol)
            
            return StockStatistics(
                symbol=symbol,
                current_price=latest_data.close,
                price_change=2.5,  # Sample data
                price_change_percent=1.2,
                volume_avg_30d=1500000,
                volatility=0.25,
                high_52w=latest_data.close * 1.5,
                low_52w=latest_data.close * 0.7,
                market_cap=150000000000  # Sample market cap
            )
            
        except Exception as e:
            logger.error(f"Error calculating statistics for {symbol}: {e}")
            return StockStatistics(symbol=symbol)
    
    async def get_ohlc_data(
        self, 
        symbol: str, 
        start_time: datetime, 
        end_time: datetime
    ) -> List[OHLCData]:
        """Get OHLC data for charting"""
        stock_data = await self.get_stock_data(symbol, start_time, end_time, interval="1d")
        
        return [
            OHLCData(
                date=data.time,
                open=data.open,
                high=data.high,
                low=data.low,
                close=data.close,
                volume=data.volume
            )
            for data in stock_data
        ]