"""Configuration settings for PEAK."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Configuration settings for PEAK application."""
    
    # Clarifai API Configuration
    clarifai_user_id: str = Field(..., env="CLARIFAI_USER_ID")
    clarifai_pat: str = Field(..., env="CLARIFAI_PAT") 
    clarifai_app_id: str = Field(..., env="CLARIFAI_APP_ID")
    clarifai_model_id: str = Field("general-image-recognition", env="CLARIFAI_MODEL_ID")
    
    # Data Paths
    data_dir: Path = Field(Path("./data"), env="DATA_DIR")
    models_dir: Path = Field(Path("./models"), env="MODELS_DIR") 
    pickle_dir: Path = Field(Path("./data/pickle"), env="PICKLE_DIR")
    dataset_dir: Path = Field(Path("./data/dataset"), env="DATASET_DIR")
    
    # Model Configuration  
    random_state: int = Field(333, env="RANDOM_STATE")
    max_depth: int = Field(13, env="MAX_DEPTH")
    n_topics: int = Field(20, env="N_TOPICS")
    
    # Topic Extraction Parameters
    tfidf_stop_words: str = Field("english", env="TFIDF_STOP_WORDS")
    nmf_init: str = Field("random", env="NMF_INIT")
    nmf_max_iter: int = Field(200, env="NMF_MAX_ITER")
    
    # Classification Parameters
    rf_n_estimators: int = Field(100, env="RF_N_ESTIMATORS")
    
    # Explanation Categories Thresholds
    dominant_threshold: float = Field(0.7, env="DOMINANT_THRESHOLD")
    opponent_threshold: float = Field(0.2, env="OPPONENT_THRESHOLD") 
    collaborative_threshold: float = Field(0.8, env="COLLABORATIVE_THRESHOLD")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    
    # Development
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("production", env="ENVIRONMENT")
    
    @validator("data_dir", "models_dir", "pickle_dir", "dataset_dir", pre=True)
    def validate_paths(cls, v):
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v)
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    @validator("log_format")
    def validate_log_format(cls, v):
        """Validate log format."""
        valid_formats = ["json", "text"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of {valid_formats}")
        return v.lower()
    
    def create_directories(self):
        """Create necessary directories if they don't exist."""
        for path in [self.data_dir, self.models_dir, self.pickle_dir, self.dataset_dir]:
            path.mkdir(parents=True, exist_ok=True)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()