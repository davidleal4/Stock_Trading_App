"""
ML Service for Stock Trading Application
Handles model training, prediction, and evaluation
"""

import asyncio
import logging
from pathlib import Path
import os

from core.config import MLConfig
from services.model_trainer import ModelTrainer
from services.prediction_service import PredictionService
from services.feature_engineer import FeatureEngineer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MLService:
    """Main ML service orchestrator"""
    
    def __init__(self):
        self.config = MLConfig()
        self.model_trainer = ModelTrainer()
        self.prediction_service = PredictionService()
        self.feature_engineer = FeatureEngineer()
        
        # Ensure models directory exists
        Path(self.config.MODEL_STORAGE_PATH).mkdir(exist_ok=True)
    
    async def start(self):
        """Start the ML service"""
        logger.info("Starting ML Service...")
        
        # Initialize components
        await self.model_trainer.initialize()
        await self.prediction_service.initialize()
        
        logger.info("ML Service started successfully")
        
        # Keep service running
        while True:
            try:
                # Check for training jobs
                await self.process_training_jobs()
                
                # Generate predictions for active models
                await self.generate_predictions()
                
                # Sleep before next iteration
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in ML service loop: {e}")
                await asyncio.sleep(30)  # Shorter sleep on error
    
    async def process_training_jobs(self):
        """Process pending model training jobs"""
        try:
            jobs = await self.model_trainer.get_pending_jobs()
            for job in jobs:
                logger.info(f"Processing training job: {job}")
                await self.model_trainer.train_model(job)
        except Exception as e:
            logger.error(f"Error processing training jobs: {e}")
    
    async def generate_predictions(self):
        """Generate predictions for active models"""
        try:
            await self.prediction_service.generate_all_predictions()
        except Exception as e:
            logger.error(f"Error generating predictions: {e}")

async def main():
    """Main entry point"""
    service = MLService()
    await service.start()

if __name__ == "__main__":
    asyncio.run(main())