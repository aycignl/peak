#!/usr/bin/env python3
"""
Advanced PEAK Pipeline Example

This script demonstrates advanced features of the PEAK system including:
- Custom configuration
- Batch processing
- Model evaluation
- Explanation generation
"""

import os
import sys
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

# Add the src directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from peak.pipeline.training_pipeline import TrainingPipeline
from peak.pipeline.inference_pipeline import InferencePipeline
from peak.config.settings import Settings
from peak.data.loaders import DataLoader
from peak.models.explanation_generation import ExplanationGenerator
from peak.utils.visualization import create_performance_plot


def load_sample_data() -> pd.DataFrame:
    """Load sample data for the example."""
    # Create sample data if actual data files are not available
    sample_data = {
        'review_text': [
            "The food was absolutely amazing! Great service and atmosphere.",
            "Terrible experience. Food was cold and service was slow.",
            "Average restaurant. Nothing special but not bad either.",
            "Fantastic pizza and excellent wine selection. Highly recommended!",
            "Overpriced for what you get. Won't be coming back.",
            "Cozy place with delicious home-made pasta. Great for families.",
            "The worst restaurant I've ever been to. Avoid at all costs.",
            "Decent food but the wait time was too long.",
            "Outstanding cuisine and impeccable service. A true gem!",
            "Good location but food quality could be much better."
        ],
        'rating': [5, 1, 3, 5, 2, 4, 1, 3, 5, 2],
        'restaurant_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'sentiment': ['positive', 'negative', 'neutral', 'positive', 'negative', 
                     'positive', 'negative', 'neutral', 'positive', 'negative']
    }
    return pd.DataFrame(sample_data)


def advanced_training_example():
    """Demonstrate advanced training pipeline features."""
    print("\n🎯 Advanced Training Pipeline")
    print("-" * 40)
    
    # Custom configuration
    config = {
        "model_config": {
            "n_topics": 5,
            "max_features": 1000,
            "random_state": 42
        },
        "training_config": {
            "test_split": 0.3,
            "validation_split": 0.2,
            "cross_validation_folds": 5
        },
        "preprocessing_config": {
            "remove_stopwords": True,
            "min_word_length": 3,
            "max_word_length": 15
        },
        "output_config": {
            "save_models": True,
            "save_metrics": True,
            "generate_plots": True
        }
    }
    
    # Initialize pipeline
    pipeline = TrainingPipeline()
    
    # Load data
    data = load_sample_data()
    print(f"📊 Loaded {len(data)} sample reviews")
    
    try:
        # Run advanced training
        results = pipeline.run_advanced(data, config)
        
        print("✅ Advanced training completed!")
        print(f"📈 Model accuracy: {results.get('accuracy', 'N/A'):.3f}")
        print(f"📊 F1-score: {results.get('f1_score', 'N/A'):.3f}")
        print(f"🎯 Topics extracted: {results.get('n_topics', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"⚠️  Training error: {e}")
        return None


def batch_inference_example():
    """Demonstrate batch inference capabilities."""
    print("\n⚡ Batch Inference Example")
    print("-" * 40)
    
    # Sample reviews for batch processing
    reviews = [
        "Amazing food and excellent service!",
        "The worst meal I've ever had.",
        "Pretty good restaurant, would recommend.",
        "Overpriced and underwhelming experience.",
        "Perfect place for a romantic dinner."
    ]
    
    try:
        # Initialize inference pipeline
        inference_pipeline = InferencePipeline()
        
        # Batch prediction
        results = inference_pipeline.predict_batch(reviews)
        
        print("📋 Batch Prediction Results:")
        for i, (review, result) in enumerate(zip(reviews, results), 1):
            print(f"\n{i}. Review: '{review[:50]}...'")
            print(f"   Prediction: {result.get('prediction', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 'N/A'):.3f}")
            print(f"   Sentiment: {result.get('sentiment', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"⚠️  Batch inference error: {e}")
        return None


def explanation_generation_example():
    """Demonstrate explanation generation features."""
    print("\n💡 Explanation Generation Example")
    print("-" * 40)
    
    try:
        # Initialize explanation generator
        explainer = ExplanationGenerator()
        
        # Sample review and prediction
        review = "The food was delicious but the service was terrible."
        prediction = "mixed"
        confidence = 0.75
        
        # Generate explanations
        explanations = explainer.generate_explanations(
            review_text=review,
            prediction=prediction,
            confidence=confidence
        )
        
        print(f"📝 Review: '{review}'")
        print(f"🎯 Prediction: {prediction} (confidence: {confidence:.2f})")
        print("\n📖 Generated Explanations:")
        
        for category, explanation in explanations.items():
            print(f"\n{category.capitalize()} Explanation:")
            print(f"  {explanation}")
        
        return explanations
        
    except Exception as e:
        print(f"⚠️  Explanation generation error: {e}")
        return None


def model_evaluation_example():
    """Demonstrate model evaluation and metrics."""
    print("\n📊 Model Evaluation Example")
    print("-" * 40)
    
    try:
        # Load sample data for evaluation
        test_data = load_sample_data()
        
        # Initialize pipeline for evaluation
        pipeline = TrainingPipeline()
        
        # Run evaluation
        metrics = pipeline.evaluate_model(test_data)
        
        print("📈 Model Performance Metrics:")
        for metric, value in metrics.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.3f}")
            else:
                print(f"  {metric}: {value}")
        
        # Generate performance plot
        plot_path = create_performance_plot(metrics)
        print(f"📊 Performance plot saved to: {plot_path}")
        
        return metrics
        
    except Exception as e:
        print(f"⚠️  Evaluation error: {e}")
        return None


def main():
    """Run all advanced examples."""
    print("🚀 PEAK System - Advanced Pipeline Examples")
    print("=" * 60)
    
    # Set up environment
    settings = Settings()
    
    # Run examples
    try:
        # 1. Advanced Training
        training_results = advanced_training_example()
        
        # 2. Batch Inference
        inference_results = batch_inference_example()
        
        # 3. Explanation Generation
        explanation_results = explanation_generation_example()
        
        # 4. Model Evaluation
        evaluation_results = model_evaluation_example()
        
        print("\n✨ All advanced examples completed!")
        print("📚 Check the outputs and logs for detailed results.")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("This is expected if the system is not fully set up.")


if __name__ == "__main__":
    main()