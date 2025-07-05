"""Clarifai API client for image tagging."""

import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from abc import ABC, abstractmethod

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from peak.config.logging_config import get_logger
from peak.config.settings import settings


logger = get_logger(__name__)


class APIClientError(Exception):
    """Custom exception for API client errors."""
    pass


class BaseTagGenerator(ABC):
    """Abstract base class for tag generators."""
    
    @abstractmethod
    def generate_tags(self, image_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Generate tags for a single image."""
        pass
    
    @abstractmethod
    def generate_tags_batch(self, image_paths: List[Union[str, Path]]) -> List[List[Dict[str, Any]]]:
        """Generate tags for multiple images."""
        pass


class MockTagGenerator(BaseTagGenerator):
    """Mock tag generator for testing purposes."""
    
    def generate_tags(self, image_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Generate mock tags for testing."""
        return [
            {"name": "test_tag_1", "value": 0.95},
            {"name": "test_tag_2", "value": 0.87},
            {"name": "test_tag_3", "value": 0.73}
        ]
    
    def generate_tags_batch(self, image_paths: List[Union[str, Path]]) -> List[List[Dict[str, Any]]]:
        """Generate mock tags for multiple images."""
        return [self.generate_tags(path) for path in image_paths]


class ClarifaiClient(BaseTagGenerator):
    """Client for Clarifai API to generate image tags."""
    
    def __init__(
        self,
        user_id: Optional[str] = None,
        pat: Optional[str] = None,
        app_id: Optional[str] = None,
        model_id: Optional[str] = None,
        model_version_id: str = "",
        rate_limit_delay: float = 0.1
    ):
        """
        Initialize Clarifai client.
        
        Args:
            user_id: Clarifai user ID (defaults to settings)
            pat: Personal Access Token (defaults to settings)
            app_id: Application ID (defaults to settings)
            model_id: Model ID (defaults to settings)
            model_version_id: Model version ID
            rate_limit_delay: Delay between API calls to respect rate limits
        """
        self.user_id = user_id or settings.clarifai_user_id
        self.pat = pat or settings.clarifai_pat
        self.app_id = app_id or settings.clarifai_app_id
        self.model_id = model_id or settings.clarifai_model_id
        self.model_version_id = model_version_id
        self.rate_limit_delay = rate_limit_delay
        
        # Initialize gRPC channel and stub
        self.channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(self.channel)
        self.metadata = (('authorization', f'Key {self.pat}'),)
        self.user_data_object = resources_pb2.UserAppIDSet(
            user_id=self.user_id, 
            app_id=self.app_id
        )
        
        logger.info("Clarifai client initialized", 
                   user_id=self.user_id, 
                   app_id=self.app_id, 
                   model_id=self.model_id)
    
    def _read_image_file(self, image_path: Union[str, Path]) -> bytes:
        """
        Read image file as bytes.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image file as bytes
            
        Raises:
            APIClientError: If file cannot be read
        """
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except Exception as e:
            raise APIClientError(f"Failed to read image file {image_path}: {e}")
    
    def generate_tags(self, image_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Generate tags for a single image using Clarifai API.
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of tag dictionaries with 'name' and 'value' keys
            
        Raises:
            APIClientError: If API call fails
        """
        logger.info("Generating tags for image", image_path=str(image_path))
        
        try:
            # Read image file
            file_bytes = self._read_image_file(image_path)
            
            # Make API request
            response = self.stub.PostModelOutputs(
                service_pb2.PostModelOutputsRequest(
                    user_app_id=self.user_data_object,
                    model_id=self.model_id,
                    version_id=self.model_version_id,
                    inputs=[
                        resources_pb2.Input(
                            data=resources_pb2.Data(
                                image=resources_pb2.Image(base64=file_bytes)
                            )
                        )
                    ]
                ),
                metadata=self.metadata
            )
            
            # Check for errors
            if response.status.code != status_code_pb2.SUCCESS:
                raise APIClientError(
                    f"Clarifai API request failed: {response.status.description}"
                )
            
            # Extract tags from response
            if not response.outputs:
                logger.warning("No outputs in API response", image_path=str(image_path))
                return []
            
            output = response.outputs[0]
            tags = [
                {"name": concept.name, "value": concept.value}
                for concept in output.data.concepts
            ]
            
            logger.info("Successfully generated tags", 
                       image_path=str(image_path), 
                       num_tags=len(tags))
            
            return tags
            
        except Exception as e:
            logger.error("Failed to generate tags", 
                        image_path=str(image_path), 
                        error=str(e))
            raise APIClientError(f"Failed to generate tags for {image_path}: {e}")
    
    def generate_tags_batch(
        self, 
        image_paths: List[Union[str, Path]], 
        max_retries: int = 3
    ) -> List[List[Dict[str, Any]]]:
        """
        Generate tags for multiple images with rate limiting and error handling.
        
        Args:
            image_paths: List of paths to image files
            max_retries: Maximum number of retries for failed requests
            
        Returns:
            List of tag lists, one for each image
        """
        logger.info("Starting batch tag generation", num_images=len(image_paths))
        
        results = []
        failed_images = []
        
        for i, image_path in enumerate(image_paths):
            retries = 0
            success = False
            
            while retries < max_retries and not success:
                try:
                    tags = self.generate_tags(image_path)
                    results.append(tags)
                    success = True
                except APIClientError as e:
                    retries += 1
                    logger.warning("API call failed, retrying", 
                                 image_path=str(image_path), 
                                 retry=retries, 
                                 error=str(e))
                    
                    if retries < max_retries:
                        time.sleep(self.rate_limit_delay * (2 ** retries))  # Exponential backoff
            
            if not success:
                logger.error("Failed to process image after retries", 
                           image_path=str(image_path))
                results.append([])
                failed_images.append(str(image_path))
            
            # Rate limiting
            if i < len(image_paths) - 1:
                time.sleep(self.rate_limit_delay)
        
        if failed_images:
            logger.warning("Some images failed to process", failed_count=len(failed_images))
        
        logger.info("Batch tag generation completed", 
                   total_images=len(image_paths), 
                   successful=len(image_paths) - len(failed_images),
                   failed=len(failed_images))
        
        return results
    
    def health_check(self) -> bool:
        """
        Perform a health check on the Clarifai API.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            # Try to list models as a simple health check
            response = self.stub.ListModels(
                service_pb2.ListModelsRequest(user_app_id=self.user_data_object),
                metadata=self.metadata
            )
            return response.status.code == status_code_pb2.SUCCESS
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return False