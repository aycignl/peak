"""Tests for configuration module."""

import pytest
from pathlib import Path
from peak.config.settings import Settings


class TestSettings:
    """Test Settings class."""
    
    def test_settings_initialization(self):
        """Test settings can be initialized with defaults."""
        settings = Settings(
            clarifai_user_id="test_user",
            clarifai_pat="test_pat", 
            clarifai_app_id="test_app"
        )
        
        assert settings.clarifai_user_id == "test_user"
        assert settings.clarifai_pat == "test_pat"
        assert settings.clarifai_app_id == "test_app"
        assert settings.n_topics == 20  # Default value
        assert settings.random_state == 333  # Default value
    
    def test_path_validation(self):
        """Test that string paths are converted to Path objects."""
        settings = Settings(
            clarifai_user_id="test_user",
            clarifai_pat="test_pat",
            clarifai_app_id="test_app",
            data_dir="./test_data"
        )
        
        assert isinstance(settings.data_dir, Path)
        assert str(settings.data_dir) == "test_data"
    
    def test_log_level_validation(self):
        """Test log level validation."""
        with pytest.raises(ValueError):
            Settings(
                clarifai_user_id="test_user",
                clarifai_pat="test_pat",
                clarifai_app_id="test_app",
                log_level="INVALID"
            )
    
    def test_create_directories(self, tmp_path):
        """Test directory creation."""
        test_data_dir = tmp_path / "test_data"
        settings = Settings(
            clarifai_user_id="test_user",
            clarifai_pat="test_pat",
            clarifai_app_id="test_app",
            data_dir=str(test_data_dir)
        )
        
        settings.create_directories()
        
        assert settings.data_dir.exists()
        assert (settings.data_dir / "dataset").exists()
        assert (settings.data_dir / "pickle").exists()