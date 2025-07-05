"""Text processing utilities for PEAK."""

import re
from typing import Any, Dict, List, Optional, Set
from collections import Counter

from peak.config.logging_config import get_logger

logger = get_logger(__name__)


class TextProcessor:
    """Text processing utilities for PEAK."""
    
    def __init__(self):
        """Initialize text processor."""
        logger.info("TextProcessor initialized")
    
    @staticmethod
    def clean_text(
        text: str,
        lowercase: bool = True,
        remove_punctuation: bool = True,
        remove_extra_spaces: bool = True
    ) -> str:
        """
        Clean text string.
        
        Args:
            text: Input text
            lowercase: Convert to lowercase
            remove_punctuation: Remove punctuation
            remove_extra_spaces: Remove extra whitespace
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Convert to lowercase
        if lowercase:
            text = text.lower()
        
        # Remove punctuation
        if remove_punctuation:
            text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra spaces
        if remove_extra_spaces:
            text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def extract_words(text: str, min_length: int = 2) -> List[str]:
        """
        Extract words from text.
        
        Args:
            text: Input text
            min_length: Minimum word length
            
        Returns:
            List of words
        """
        if not isinstance(text, str):
            text = str(text)
        
        # Split and filter words
        words = text.split()
        words = [word for word in words if len(word) >= min_length]
        
        return words
    
    @staticmethod
    def get_word_frequency(
        texts: List[str],
        top_n: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Get word frequency across multiple texts.
        
        Args:
            texts: List of text strings
            top_n: Return only top N words
            
        Returns:
            Dictionary of word frequencies
        """
        all_words = []
        
        for text in texts:
            words = TextProcessor.extract_words(
                TextProcessor.clean_text(text)
            )
            all_words.extend(words)
        
        word_freq = Counter(all_words)
        
        if top_n:
            word_freq = dict(word_freq.most_common(top_n))
        else:
            word_freq = dict(word_freq)
        
        logger.info("Word frequency calculated",
                   total_words=len(all_words),
                   unique_words=len(word_freq))
        
        return word_freq
    
    @staticmethod
    def remove_stopwords(
        text: str,
        stopwords: Optional[Set[str]] = None
    ) -> str:
        """
        Remove stopwords from text.
        
        Args:
            text: Input text
            stopwords: Set of stopwords to remove
            
        Returns:
            Text with stopwords removed
        """
        if stopwords is None:
            # Basic English stopwords
            stopwords = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
                'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
                'will', 'would', 'could', 'should', 'may', 'might', 'must',
                'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
            }
        
        words = TextProcessor.extract_words(text)
        filtered_words = [word for word in words if word.lower() not in stopwords]
        
        return ' '.join(filtered_words)
    
    @staticmethod
    def tag_intersection(
        tags1: List[str],
        tags2: List[str],
        sort_by_first: bool = True
    ) -> List[str]:
        """
        Find intersection of two tag lists.
        
        Args:
            tags1: First tag list
            tags2: Second tag list
            sort_by_first: Sort result by order in first list
            
        Returns:
            List of common tags
        """
        set1 = set(tags1)
        set2 = set(tags2)
        common = set1.intersection(set2)
        
        if sort_by_first:
            # Maintain order from first list
            result = [tag for tag in tags1 if tag in common]
        else:
            result = list(common)
        
        return result
    
    @staticmethod
    def format_tag_list(
        tags: List[str],
        max_tags: Optional[int] = None,
        separator: str = ", "
    ) -> str:
        """
        Format tag list as string.
        
        Args:
            tags: List of tags
            max_tags: Maximum number of tags to include
            separator: Separator between tags
            
        Returns:
            Formatted tag string
        """
        if max_tags and len(tags) > max_tags:
            tags = tags[:max_tags]
        
        return separator.join(tags)
    
    @staticmethod
    def parse_tag_string(
        tag_string: str,
        separator: Optional[str] = None
    ) -> List[str]:
        """
        Parse tag string into list.
        
        Args:
            tag_string: String containing tags
            separator: Tag separator (auto-detect if None)
            
        Returns:
            List of tags
        """
        if not isinstance(tag_string, str):
            tag_string = str(tag_string)
        
        # Auto-detect separator if not provided
        if separator is None:
            if ',' in tag_string:
                separator = ','
            elif ';' in tag_string:
                separator = ';'
            else:
                separator = ' '
        
        # Split and clean tags
        tags = tag_string.split(separator)
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        return tags