"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/stock_trading",
        description="Database connection URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # API Keys for data sources
    EODHD_API_KEY: str = Field(default="", description="EODHD API key")
    POLYGON_API_KEY: str = Field(default="", description="Polygon API key")
    ALPHA_VANTAGE_API_KEY: str = Field(default="", description="Alpha Vantage API key")
    
    # Fidelity API (sandbox by default)
    FIDELITY_API_KEY: str = Field(default="", description="Fidelity API key")
    FIDELITY_API_SECRET: str = Field(default="", description="Fidelity API secret")
    FIDELITY_SANDBOX: bool = Field(default=True, description="Use Fidelity sandbox")
    
    # OpenAI API (optional for enhanced AI features)
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    
    # Default stock symbols
    DEFAULT_SYMBOLS: List[str] = Field(
        default=["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA", "BRK.B", "JPM", "V"],
        description="Default stock symbols to track"
    )
    
    # ML Model settings
    MODEL_STORAGE_PATH: str = Field(
        default="./models",
        description="Path to store ML models"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()