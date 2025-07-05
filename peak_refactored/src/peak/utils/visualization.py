"""Visualization utilities for PEAK."""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from peak.config.logging_config import get_logger

logger = get_logger(__name__)


class Visualizer:
    """Visualization utilities for PEAK analysis."""
    
    def __init__(self, style: str = "whitegrid"):
        """
        Initialize visualizer.
        
        Args:
            style: Seaborn style to use
        """
        sns.set_style(style)
        plt.style.use('default')
        logger.info("Visualizer initialized", style=style)
    
    @staticmethod
    def plot_label_distribution(
        labels: pd.Series,
        title: str = "Privacy Label Distribution",
        figsize: Tuple[int, int] = (8, 6)
    ) -> plt.Figure:
        """
        Plot distribution of privacy labels.
        
        Args:
            labels: Series of privacy labels
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Count labels
        label_counts = labels.value_counts()
        label_names = ['Private' if x == 0 else 'Public' for x in label_counts.index]
        
        # Create bar plot
        bars = ax.bar(label_names, label_counts.values)
        
        # Add value labels on bars
        for bar, count in zip(bars, label_counts.values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(label_counts),
                   f'{count}', ha='center', va='bottom')
        
        ax.set_title(title)
        ax.set_ylabel('Count')
        ax.set_xlabel('Privacy Label')
        
        plt.tight_layout()
        logger.info("Label distribution plot created")
        
        return fig
    
    @staticmethod
    def plot_feature_importance(
        feature_importance: Dict[str, float],
        title: str = "Feature Importance",
        top_n: int = 10,
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            feature_importance: Dictionary of feature names and importance scores
            title: Plot title
            top_n: Number of top features to show
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        # Sort features by importance
        sorted_features = sorted(feature_importance.items(), 
                               key=lambda x: x[1], reverse=True)[:top_n]
        
        features, importance = zip(*sorted_features)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create horizontal bar plot
        y_pos = np.arange(len(features))
        bars = ax.barh(y_pos, importance)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(features)
        ax.invert_yaxis()  # Top feature at top
        ax.set_xlabel('Importance Score')
        ax.set_title(title)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, importance)):
            width = bar.get_width()
            ax.text(width + 0.01*max(importance), bar.get_y() + bar.get_height()/2,
                   f'{score:.3f}', ha='left', va='center')
        
        plt.tight_layout()
        logger.info("Feature importance plot created", num_features=len(features))
        
        return fig
    
    @staticmethod
    def plot_topic_distribution(
        topic_features: np.ndarray,
        topic_names: Optional[List[str]] = None,
        title: str = "Topic Distribution",
        figsize: Tuple[int, int] = (12, 8)
    ) -> plt.Figure:
        """
        Plot distribution of topic features.
        
        Args:
            topic_features: Array of topic features (samples x topics)
            topic_names: Names of topics
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        n_topics = topic_features.shape[1]
        
        if topic_names is None:
            topic_names = [f"Topic {i}" for i in range(n_topics)]
        
        # Calculate mean topic values
        topic_means = np.mean(topic_features, axis=0)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Plot 1: Mean topic values
        ax1.bar(range(n_topics), topic_means)
        ax1.set_xlabel('Topic')
        ax1.set_ylabel('Mean Value')
        ax1.set_title('Average Topic Strength')
        ax1.set_xticks(range(n_topics))
        ax1.set_xticklabels([f"T{i}" for i in range(n_topics)], rotation=45)
        
        # Plot 2: Topic distribution heatmap
        im = ax2.imshow(topic_features[:50].T, aspect='auto', cmap='viridis')
        ax2.set_xlabel('Sample')
        ax2.set_ylabel('Topic')
        ax2.set_title('Topic Values (First 50 samples)')
        ax2.set_yticks(range(min(n_topics, 20)))
        ax2.set_yticklabels([f"T{i}" for i in range(min(n_topics, 20))])
        
        plt.colorbar(im, ax=ax2)
        plt.suptitle(title)
        plt.tight_layout()
        
        logger.info("Topic distribution plot created", n_topics=n_topics)
        
        return fig
    
    @staticmethod
    def plot_confusion_matrix(
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Confusion Matrix",
        figsize: Tuple[int, int] = (8, 6)
    ) -> plt.Figure:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        from sklearn.metrics import confusion_matrix
        
        cm = confusion_matrix(y_true, y_pred)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=['Private', 'Public'],
                   yticklabels=['Private', 'Public'])
        
        ax.set_title(title)
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
        
        plt.tight_layout()
        logger.info("Confusion matrix plot created")
        
        return fig
    
    @staticmethod
    def plot_explanation_categories(
        categories: Dict[str, List[int]],
        title: str = "Explanation Categories Distribution",
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Plot distribution of explanation categories.
        
        Args:
            categories: Dictionary mapping category names to sample indices
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        category_names = list(categories.keys())
        category_counts = [len(indices) for indices in categories.values()]
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create pie chart
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        wedges, texts, autotexts = ax.pie(category_counts, labels=category_names,
                                         autopct='%1.1f%%', colors=colors[:len(category_names)])
        
        ax.set_title(title)
        
        # Add count information
        for i, (name, count) in enumerate(zip(category_names, category_counts)):
            ax.text(0.5, -1.3 - i*0.1, f"{name}: {count} samples", 
                   transform=ax.transAxes, ha='center')
        
        plt.tight_layout()
        logger.info("Explanation categories plot created", 
                   categories=dict(zip(category_names, category_counts)))
        
        return fig
    
    @staticmethod
    def plot_training_history(
        history: Dict[str, List[float]],
        title: str = "Training History",
        figsize: Tuple[int, int] = (12, 4)
    ) -> plt.Figure:
        """
        Plot training history metrics.
        
        Args:
            history: Dictionary with metric names and values over epochs
            title: Plot title
            figsize: Figure size
            
        Returns:
            matplotlib Figure object
        """
        n_metrics = len(history)
        fig, axes = plt.subplots(1, n_metrics, figsize=figsize)
        
        if n_metrics == 1:
            axes = [axes]
        
        for i, (metric_name, values) in enumerate(history.items()):
            axes[i].plot(values)
            axes[i].set_title(f'{metric_name.title()}')
            axes[i].set_xlabel('Epoch')
            axes[i].set_ylabel(metric_name.title())
            axes[i].grid(True)
        
        plt.suptitle(title)
        plt.tight_layout()
        
        logger.info("Training history plot created", metrics=list(history.keys()))
        
        return fig
    
    @staticmethod
    def save_plot(
        fig: plt.Figure,
        filepath: str,
        dpi: int = 300,
        bbox_inches: str = 'tight'
    ) -> None:
        """
        Save plot to file.
        
        Args:
            fig: matplotlib Figure object
            filepath: Output file path
            dpi: DPI for saved image
            bbox_inches: Bounding box setting
        """
        fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
        logger.info("Plot saved", filepath=filepath, dpi=dpi)