"""
PEAK: Explainable Privacy Assistant through Automated Knowledge Extraction

A machine learning pipeline for privacy classification and explanation generation.
"""

__version__ = "1.0.0"
__author__ = "Ayca Gonul"
__email__ = "gonul.ayci@boun.edu.tr"

from peak.config.settings import Settings
from peak.pipeline.training_pipeline import TrainingPipeline
from peak.pipeline.inference_pipeline import InferencePipeline
from peak.models.topic_extraction import TopicExtractor
from peak.models.classification import PrivacyClassifier
from peak.models.explanation_generation import ExplanationGenerator

__all__ = [
    "Settings",
    "TrainingPipeline", 
    "InferencePipeline",
    "TopicExtractor",
    "PrivacyClassifier", 
    "ExplanationGenerator",
]