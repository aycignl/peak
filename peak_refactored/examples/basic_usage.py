#!/usr/bin/env python3
"""
Basic PEAK Usage Example

This script demonstrates the basic usage of the PEAK system for restaurant review analysis.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from peak.pipeline.training_pipeline import TrainingPipeline
from peak.pipeline.inference_pipeline import InferencePipeline
from peak.config.settings import Settings
from peak.data.loaders import DataLoader


def main():
    """Basic usage example of the PEAK system."""
    
    # Initialize settings
    settings = Settings()
    print("🚀 PEAK System - Basic Usage Example")
    print("=" * 50)
    
    # 1. Data Loading Example
    print("\n📊 Loading Data...")
    loader = DataLoader()
    
    # Load CSV data
    train_data_path = project_root / "data" / "df_train.csv"
    if train_data_path.exists():
        train_data = loader.load_csv(str(train_data_path))
        print(f"✅ Loaded training data: {train_data.shape}")
    else:
        print("⚠️  Training data not found. Please ensure data files are in the data/ directory.")
        return
    
    # 2. Training Pipeline Example
    print("\n🔄 Training Pipeline...")
    try:
        training_pipeline = TrainingPipeline()
        
        # Configure pipeline
        pipeline_config = {
            "data_path": str(train_data_path),
            "test_split": 0.2,
            "random_state": 42,
            "n_topics": 5,
            "enable_checkpointing": True
        }
        
        # Run training (with sample data for demo)
        print("Training models... (this may take a few minutes)")
        results = training_pipeline.run(config=pipeline_config)
        print(f"✅ Training completed. Models saved to: {results.get('model_path', 'models/')}")
        
    except Exception as e:
        print(f"⚠️  Training pipeline error: {e}")
        print("This is expected if running without proper data setup.")
    
    # 3. Inference Pipeline Example
    print("\n🔍 Inference Pipeline...")
    try:
        inference_pipeline = InferencePipeline()
        
        # Sample review for prediction
        sample_review = "The food was amazing and the service was excellent!"
        
        # Run inference
        results = inference_pipeline.predict_single(sample_review)
        
        print(f"📝 Sample Review: '{sample_review}'")
        print(f"🎯 Prediction: {results.get('prediction', 'N/A')}")
        print(f"📈 Confidence: {results.get('confidence', 'N/A')}")
        print(f"💡 Explanation: {results.get('explanation', 'N/A')}")
        
    except Exception as e:
        print(f"⚠️  Inference pipeline error: {e}")
        print("This is expected if models haven't been trained yet.")
    
    # 4. Topic Extraction Example
    print("\n🏷️  Topic Extraction...")
    try:
        from peak.models.topic_extraction import TopicExtractor
        
        topic_extractor = TopicExtractor(n_topics=3)
        
        # Sample reviews for topic extraction
        sample_reviews = [
            "The pizza was delicious and the atmosphere was great",
            "Terrible service, food was cold and overpriced",
            "Amazing pasta, friendly staff, highly recommended"
        ]
        
        topics = topic_extractor.extract_topics(sample_reviews)
        print("📋 Extracted Topics:")
        for i, topic in enumerate(topics[:3]):  # Show first 3 topics
            print(f"  Topic {i+1}: {topic}")
            
    except Exception as e:
        print(f"⚠️  Topic extraction error: {e}")
    
    print("\n✨ Basic usage example completed!")
    print("📚 For more advanced examples, check the other files in the examples/ directory.")


if __name__ == "__main__":
    main()