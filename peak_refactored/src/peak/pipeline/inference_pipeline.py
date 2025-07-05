"""Inference pipeline for PEAK."""

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


class InferencePipeline(BasePipeline):
    """Inference pipeline for PEAK predictions and explanations."""
    
    def __init__(
        self,
        models_dir: Optional[Union[str, Path]] = None,
        checkpoint_dir: Optional[Union[str, Path]] = None
    ):
        """
        Initialize inference pipeline.
        
        Args:
            models_dir: Directory containing trained models
            checkpoint_dir: Directory for pipeline checkpoints
        """
        super().__init__("inference_pipeline", checkpoint_dir)
        
        self.models_dir = Path(models_dir) if models_dir else settings.models_dir
        
        # Model components (loaded on demand)
        self.topic_extractor = None
        self.classifier = None
        self.models_loaded = False
        
        logger.info("Inference pipeline initialized", models_dir=str(self.models_dir))
    
    def load_models(
        self,
        topic_extractor_path: Optional[Union[str, Path]] = None,
        classifier_path: Optional[Union[str, Path]] = None
    ) -> None:
        """
        Load trained models.
        
        Args:
            topic_extractor_path: Path to topic extractor model
            classifier_path: Path to classifier model
        """
        logger.info("Loading trained models")
        
        try:
            # Default paths
            if not topic_extractor_path:
                topic_extractor_path = self.models_dir / "topic_extractor.pkl"
            if not classifier_path:
                classifier_path = self.models_dir / "privacy_classifier.pkl"
            
            # Load topic extractor
            self.topic_extractor = TopicExtractor()
            self.topic_extractor.load_model(topic_extractor_path)
            
            # Load classifier
            self.classifier = PrivacyClassifier()
            self.classifier.load_model(classifier_path)
            
            self.models_loaded = True
            
            logger.info("Models loaded successfully",
                       topic_extractor_path=str(topic_extractor_path),
                       classifier_path=str(classifier_path))
            
        except Exception as e:
            raise PipelineError(f"Failed to load models: {e}")
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Run inference pipeline - alias for predict method.
        
        Returns:
            Dictionary with prediction results
        """
        return self.predict(**kwargs)
    
    def predict(
        self,
        data: Union[pd.DataFrame, List[str], str],
        return_probabilities: bool = False,
        return_explanations: bool = False,
        batch_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make predictions on new data.
        
        Args:
            data: Input data (DataFrame with 'cleaned_tags' column, list of tag strings, or single string)
            return_probabilities: Whether to return prediction probabilities
            return_explanations: Whether to return SHAP explanations
            batch_size: Batch size for processing (for large datasets)
            
        Returns:
            Dictionary with predictions and optional probabilities/explanations
        """
        if not self.models_loaded:
            raise PipelineError("Models not loaded. Call load_models() first.")
        
        try:
            self.start()
            
            # Step 1: Prepare input data
            documents = self._prepare_input_data(data)
            
            # Step 2: Extract features
            features = self._extract_features(documents)
            
            # Step 3: Make predictions
            predictions = self._make_predictions(features)
            
            results = {"predictions": predictions}
            
            # Step 4: Get probabilities (optional)
            if return_probabilities:
                probabilities = self._get_probabilities(features)
                results["probabilities"] = probabilities
            
            # Step 5: Generate explanations (optional)
            if return_explanations:
                explanations = self._generate_explanations(features, documents)
                results["explanations"] = explanations
            
            self.finish()
            results["pipeline_status"] = self.get_status()
            
            logger.info("Inference completed successfully",
                       num_samples=len(predictions))
            
            return results
            
        except Exception as e:
            logger.error("Inference pipeline failed", error=str(e))
            raise PipelineError(f"Inference pipeline failed: {e}")
    
    def predict_single(
        self,
        text: str,
        return_probabilities: bool = False,
        return_explanation: bool = False
    ) -> Dict[str, Any]:
        """
        Make prediction for a single text input.
        
        Args:
            text: Input text (cleaned tags)
            return_probabilities: Whether to return prediction probabilities
            return_explanation: Whether to return SHAP explanation
            
        Returns:
            Dictionary with prediction result
        """
        results = self.predict(
            data=text,
            return_probabilities=return_probabilities,
            return_explanations=return_explanation
        )
        
        # Extract single result
        single_result = {
            "prediction": results["predictions"][0]
        }
        
        if return_probabilities:
            single_result["probabilities"] = results["probabilities"][0]
        
        if return_explanation and "explanations" in results:
            single_result["explanation"] = results["explanations"][0]
        
        return single_result
    
    def _prepare_input_data(self, data: Union[pd.DataFrame, List[str], str]) -> List[str]:
        """
        Prepare input data for processing.
        
        Args:
            data: Input data in various formats
            
        Returns:
            List of document strings
        """
        if isinstance(data, str):
            # Single string input
            return [data]
        
        elif isinstance(data, list):
            # List of strings
            return data
        
        elif isinstance(data, pd.DataFrame):
            # DataFrame with 'cleaned_tags' column
            if 'cleaned_tags' not in data.columns:
                raise PipelineError("'cleaned_tags' column not found in input DataFrame")
            return data['cleaned_tags'].tolist()
        
        else:
            raise PipelineError(f"Unsupported input data type: {type(data)}")
    
    def _extract_features(self, documents: List[str]) -> np.ndarray:
        """
        Extract features from documents using trained topic extractor.
        
        Args:
            documents: List of text documents
            
        Returns:
            Feature matrix
        """
        logger.info("Extracting features from documents", num_documents=len(documents))
        
        try:
            features = self.topic_extractor.transform(documents)
            self.add_step("extract_features")
            
            logger.info("Feature extraction completed", features_shape=features.shape)
            return features
            
        except Exception as e:
            raise PipelineError(f"Failed to extract features: {e}")
    
    def _make_predictions(self, features: np.ndarray) -> List[int]:
        """
        Make predictions using trained classifier.
        
        Args:
            features: Input features
            
        Returns:
            List of predictions
        """
        logger.info("Making predictions", num_samples=features.shape[0])
        
        try:
            predictions = self.classifier.predict(features)
            self.add_step("make_predictions")
            
            logger.info("Predictions completed", num_predictions=len(predictions))
            return predictions.tolist()
            
        except Exception as e:
            raise PipelineError(f"Failed to make predictions: {e}")
    
    def _get_probabilities(self, features: np.ndarray) -> List[List[float]]:
        """
        Get prediction probabilities.
        
        Args:
            features: Input features
            
        Returns:
            List of probability arrays
        """
        logger.info("Getting prediction probabilities")
        
        try:
            probabilities = self.classifier.predict_proba(features)
            self.add_step("get_probabilities")
            
            return probabilities.tolist()
            
        except Exception as e:
            raise PipelineError(f"Failed to get probabilities: {e}")
    
    def _generate_explanations(
        self, 
        features: np.ndarray, 
        documents: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate SHAP explanations for predictions.
        
        Args:
            features: Input features
            documents: Original text documents
            
        Returns:
            List of explanation dictionaries
        """
        logger.info("Generating explanations", num_samples=features.shape[0])
        
        try:
            explanations = []
            
            for i in range(features.shape[0]):
                explanation = self.classifier.explain_prediction(features, sample_idx=i)
                explanation["original_text"] = documents[i]
                explanations.append(explanation)
            
            self.add_step("generate_explanations")
            
            logger.info("Explanations generated", num_explanations=len(explanations))
            return explanations
            
        except Exception as e:
            raise PipelineError(f"Failed to generate explanations: {e}")
    
    def predict_from_file(
        self,
        input_file: Union[str, Path],
        output_file: Optional[Union[str, Path]] = None,
        return_probabilities: bool = False,
        return_explanations: bool = False
    ) -> Dict[str, Any]:
        """
        Make predictions from input file and optionally save to output file.
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file (optional)
            return_probabilities: Whether to include probabilities
            return_explanations: Whether to include explanations
            
        Returns:
            Dictionary with prediction results
        """
        logger.info("Making predictions from file", input_file=str(input_file))
        
        try:
            # Load data from file
            input_df = pd.read_csv(input_file)
            
            # Make predictions
            results = self.predict(
                data=input_df,
                return_probabilities=return_probabilities,
                return_explanations=return_explanations
            )
            
            # Create output DataFrame
            output_df = input_df.copy()
            output_df['predicted_privacy'] = results["predictions"]
            
            if return_probabilities:
                probabilities = np.array(results["probabilities"])
                output_df['probability_private'] = probabilities[:, 0]
                output_df['probability_public'] = probabilities[:, 1]
            
            if return_explanations:
                # Add top contributing topics as explanation summary
                explanations = results["explanations"]
                explanation_summaries = []
                
                for exp in explanations:
                    # Get top 3 most important features
                    shap_values = np.array(exp["shap_values"][0])
                    feature_names = exp["feature_names"]
                    
                    # Get indices of top features by absolute SHAP value
                    top_indices = np.argsort(np.abs(shap_values))[-3:][::-1]
                    top_features = [feature_names[i] for i in top_indices]
                    
                    explanation_summaries.append(", ".join(top_features))
                
                output_df['explanation_summary'] = explanation_summaries
            
            # Save to file if specified
            if output_file:
                output_df.to_csv(output_file, index=False)
                logger.info("Predictions saved to file", output_file=str(output_file))
            
            results["output_dataframe"] = output_df
            
            return results
            
        except Exception as e:
            raise PipelineError(f"Failed to process file: {e}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about loaded models.
        
        Returns:
            Dictionary with model information
        """
        if not self.models_loaded:
            return {"models_loaded": False}
        
        return {
            "models_loaded": True,
            "topic_extractor_info": self.topic_extractor.get_model_info(),
            "classifier_info": self.classifier.get_model_info()
        }