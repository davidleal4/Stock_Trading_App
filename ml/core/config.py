"""
ML Configuration settings
"""

import os
from typing import Dict, Any

class MLConfig:
    """ML Service configuration"""
    
    def __init__(self):
        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/stock_trading")
        
        # Redis
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Model storage
        self.MODEL_STORAGE_PATH = os.getenv("MODEL_STORAGE_PATH", "./models")
        
        # Default symbols to train models for
        self.DEFAULT_SYMBOLS = ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "TSLA", "BRK.B", "JPM", "V"]
        
        # Model configurations
        self.MODEL_CONFIGS = {
            "lightgbm": {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 6,
                "num_leaves": 31,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "random_state": 42,
            },
            "xgboost": {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 6,
                "subsample": 0.8,
                "colsample_bytree": 0.8,
                "random_state": 42,
            },
            "catboost": {
                "iterations": 100,
                "learning_rate": 0.1,
                "depth": 6,
                "random_seed": 42,
                "verbose": False,
            },
            "lstm": {
                "hidden_size": 50,
                "num_layers": 2,
                "dropout": 0.2,
                "sequence_length": 60,
                "batch_size": 32,
                "epochs": 50,
                "learning_rate": 0.001,
            }
        }
        
        # Feature engineering settings
        self.FEATURE_CONFIG = {
            "lookback_windows": [5, 10, 20, 50],
            "technical_indicators": ["rsi", "macd", "bollinger", "sma", "ema"],
            "lag_features": [1, 2, 3, 5, 10],
            "price_features": ["open", "high", "low", "close", "volume"],
        }
        
        # Training settings
        self.TRAINING_CONFIG = {
            "test_size": 0.2,
            "validation_size": 0.1,
            "min_training_samples": 1000,
            "retrain_frequency_hours": 24,
        }