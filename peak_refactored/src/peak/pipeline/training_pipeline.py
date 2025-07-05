"""Training pipeline for PEAK."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from peak.config.logging_config import get_logger
from peak.config.settings import settings
from peak.data.loaders import DataLoader
from peak.models.topic_extraction import TopicExtractor
from peak.models.classification import PrivacyClassifier
from peak.pipeline.base import BasePipeline, PipelineError

logger = get_logger(__name__)


class TrainingPipeline(BasePipeline):
    """Complete training pipeline for PEAK."""
    
    def __init__(
        self,
        data_dir: Optional[Union[str, Path]] = None,
        models_dir: Optional[Union[str, Path]] = None,
        checkpoint_dir: Optional[Union[str, Path]] = None,
        n_topics: Optional[int] = None,
        random_state: Optional[int] = None
    ):
        """
        Initialize training pipeline.
        
        Args:
            data_dir: Directory containing training data
            models_dir: Directory to save trained models
            checkpoint_dir: Directory for pipeline checkpoints
            n_topics: Number of topics for extraction
            random_state: Random state for reproducibility
        """
        super().__init__("training_pipeline", checkpoint_dir)
        
        self.data_dir = Path(data_dir) if data_dir else settings.data_dir
        self.models_dir = Path(models_dir) if models_dir else settings.models_dir
        self.n_topics = n_topics or settings.n_topics
        self.random_state = random_state or settings.random_state
        
        # Ensure directories exist
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.data_loader = DataLoader(self.data_dir)
        self.topic_extractor = TopicExtractor(
            n_topics=self.n_topics,
            random_state=self.random_state
        )
        self.classifier = PrivacyClassifier(random_state=self.random_state)
        
        # Pipeline state
        self.train_df = None
        self.test_df = None
        self.train_features = None
        self.test_features = None
        self.train_labels = None
        self.test_labels = None
        
        logger.info("Training pipeline initialized",
                   data_dir=str(self.data_dir),
                   models_dir=str(self.models_dir),
                   n_topics=self.n_topics)
    
    def run(
        self,
        save_models: bool = True,
        evaluate: bool = True,
        save_processed_data: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete training pipeline.
        
        Args:
            save_models: Whether to save trained models
            evaluate: Whether to evaluate model performance
            save_processed_data: Whether to save processed features
            
        Returns:
            Dictionary with training results and metrics
        """
        try:
            self.start()
            
            # Step 1: Load data
            results = self._load_data()
            
            # Step 2: Extract topics and create features
            self._extract_topics()
            
            # Step 3: Prepare labels
            self._prepare_labels()
            
            # Step 4: Train classifier
            training_metrics = self._train_classifier()
            results.update(training_metrics)
            
            # Step 5: Evaluate model (optional)
            if evaluate:
                evaluation_metrics = self._evaluate_model()
                results.update(evaluation_metrics)
            
            # Step 6: Save models (optional)
            if save_models:
                model_paths = self._save_models()
                results["model_paths"] = model_paths
            
            # Step 7: Save processed data (optional)
            if save_processed_data:
                self._save_processed_data()
            
            self.finish()
            results["pipeline_status"] = self.get_status()
            
            logger.info("Training pipeline completed successfully")
            return results
            
        except Exception as e:
            logger.error("Training pipeline failed", error=str(e))
            raise PipelineError(f"Training pipeline failed: {e}")
    
    def _load_data(self) -> Dict[str, Any]:
        """Load training and test data."""
        logger.info("Loading training data")
        
        try:
            self.train_df, self.test_df = self.data_loader.load_training_data()
            
            # Save checkpoint
            self.save_checkpoint({
                "train_df": self.train_df,
                "test_df": self.test_df
            }, "data_loaded")
            
            self.add_step("load_data")
            
            return {
                "train_samples": len(self.train_df),
                "test_samples": len(self.test_df),
                "train_columns": list(self.train_df.columns),
                "test_columns": list(self.test_df.columns)
            }
            
        except Exception as e:
            raise PipelineError(f"Failed to load data: {e}")
    
    def _extract_topics(self) -> None:
        """Extract topics using NMF and TF-IDF."""
        logger.info("Extracting topics from text data")
        
        try:
            # Check if cleaned_tags column exists
            if 'cleaned_tags' not in self.train_df.columns:
                raise PipelineError("'cleaned_tags' column not found in training data")
            
            # Fit topic extractor on training data
            train_documents = self.train_df['cleaned_tags'].tolist()
            self.train_features = self.topic_extractor.fit_transform(train_documents)
            
            # Transform test data
            test_documents = self.test_df['cleaned_tags'].tolist()
            self.test_features = self.topic_extractor.transform(test_documents)
            
            # Save checkpoint
            self.save_checkpoint({
                "topic_extractor": self.topic_extractor,
                "train_features": self.train_features,
                "test_features": self.test_features
            }, "topics_extracted")
            
            self.add_step("extract_topics")
            
            logger.info("Topic extraction completed",
                       train_features_shape=self.train_features.shape,
                       test_features_shape=self.test_features.shape,
                       n_topics=self.n_topics)
            
        except Exception as e:
            raise PipelineError(f"Failed to extract topics: {e}")
    
    def _prepare_labels(self) -> None:
        """Prepare labels for classification."""
        logger.info("Preparing classification labels")
        
        try:
            # Check if label column exists
            if 'normalizedpublic' not in self.train_df.columns:
                raise PipelineError("'normalizedpublic' column not found in training data")
            
            # Prepare labels using topic extractor utility
            self.train_labels = self.topic_extractor.prepare_labels(
                self.train_df['normalizedpublic'].values
            )
            self.test_labels = self.topic_extractor.prepare_labels(
                self.test_df['normalizedpublic'].values
            )
            
            self.add_step("prepare_labels")
            
            logger.info("Labels prepared",
                       train_labels_shape=self.train_labels.shape,
                       test_labels_shape=self.test_labels.shape,
                       unique_train_labels=np.unique(self.train_labels),
                       unique_test_labels=np.unique(self.test_labels))
            
        except Exception as e:
            raise PipelineError(f"Failed to prepare labels: {e}")
    
    def _train_classifier(self) -> Dict[str, Any]:
        """Train the privacy classifier."""
        logger.info("Training privacy classifier")
        
        try:
            # Create feature names
            feature_names = [f"topic_{i}" for i in range(self.n_topics)]
            
            # Train classifier
            self.classifier.fit(
                self.train_features,
                self.train_labels,
                feature_names=feature_names
            )
            
            # Save checkpoint
            self.save_checkpoint({
                "classifier": self.classifier
            }, "classifier_trained")
            
            self.add_step("train_classifier")
            
            # Get feature importance
            feature_importance = self.classifier.get_feature_importance()
            
            return {
                "feature_importance": feature_importance,
                "n_features": self.train_features.shape[1]
            }
            
        except Exception as e:
            raise PipelineError(f"Failed to train classifier: {e}")
    
    def _evaluate_model(self) -> Dict[str, Any]:
        """Evaluate the trained model."""
        logger.info("Evaluating model performance")
        
        try:
            # Evaluate on test set
            evaluation = self.classifier.evaluate(self.test_features, self.test_labels)
            
            self.add_step("evaluate_model")
            
            logger.info("Model evaluation completed",
                       test_accuracy=evaluation['accuracy'])
            
            return {"evaluation": evaluation}
            
        except Exception as e:
            raise PipelineError(f"Failed to evaluate model: {e}")
    
    def _save_models(self) -> Dict[str, str]:
        """Save trained models."""
        logger.info("Saving trained models")
        
        try:
            # Save topic extractor
            topic_extractor_path = self.models_dir / "topic_extractor.pkl"
            self.topic_extractor.save_model(topic_extractor_path)
            
            # Save classifier
            classifier_path = self.models_dir / "privacy_classifier.pkl"
            self.classifier.save_model(classifier_path)
            
            self.add_step("save_models")
            
            model_paths = {
                "topic_extractor": str(topic_extractor_path),
                "classifier": str(classifier_path)
            }
            
            logger.info("Models saved successfully", model_paths=model_paths)
            
            return model_paths
            
        except Exception as e:
            raise PipelineError(f"Failed to save models: {e}")
    
    def _save_processed_data(self) -> None:
        """Save processed features and labels."""
        logger.info("Saving processed features and labels")
        
        try:
            self.data_loader.save_processed_features(
                self.train_features,
                self.test_features,
                self.train_labels,
                self.test_labels
            )
            
            self.add_step("save_processed_data")
            
            logger.info("Processed data saved successfully")
            
        except Exception as e:
            raise PipelineError(f"Failed to save processed data: {e}")
    
    def resume_from_checkpoint(self, checkpoint_name: str) -> bool:
        """
        Resume pipeline from a checkpoint.
        
        Args:
            checkpoint_name: Name of checkpoint to resume from
            
        Returns:
            True if successfully resumed, False otherwise
        """
        logger.info("Attempting to resume from checkpoint", checkpoint_name=checkpoint_name)
        
        checkpoint_data = self.load_checkpoint(checkpoint_name)
        if not checkpoint_data:
            return False
        
        try:
            if checkpoint_name == "data_loaded":
                self.train_df = checkpoint_data["train_df"]
                self.test_df = checkpoint_data["test_df"]
                
            elif checkpoint_name == "topics_extracted":
                self.topic_extractor = checkpoint_data["topic_extractor"]
                self.train_features = checkpoint_data["train_features"]
                self.test_features = checkpoint_data["test_features"]
                
            elif checkpoint_name == "classifier_trained":
                self.classifier = checkpoint_data["classifier"]
            
            logger.info("Successfully resumed from checkpoint", checkpoint_name=checkpoint_name)
            return True
            
        except Exception as e:
            logger.error("Failed to resume from checkpoint", 
                        checkpoint_name=checkpoint_name,
                        error=str(e))
            return False