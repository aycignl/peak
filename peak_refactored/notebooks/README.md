# Notebooks Directory

This directory contains the original Jupyter notebooks from the PEAK system, preserved for reference and comparison with the refactored code.

## Original Notebooks

### 1. `extract_topics.ipynb`
- **Purpose**: Topic extraction from restaurant reviews using NMF (Non-negative Matrix Factorization)
- **Key Features**:
  - Text preprocessing and cleaning
  - TF-IDF vectorization
  - Topic modeling with NMF
  - Topic visualization and analysis
- **Refactored To**: `src/peak/models/topic_extraction.py` and `src/peak/pipeline/training_pipeline.py`

### 2. `classify_images.ipynb`
- **Purpose**: Image classification using Clarifai API for restaurant images
- **Key Features**:
  - Integration with Clarifai API
  - Image processing and classification
  - Feature extraction from images
- **Refactored To**: `src/peak/api/clarifai_client.py` and related pipeline components

### 3. `generate_explanations.ipynb`
- **Purpose**: Generate explanations for model predictions
- **Key Features**:
  - SHAP (SHapley Additive exPlanations) value analysis
  - Feature importance calculation
  - Human-readable explanation generation
- **Refactored To**: `src/peak/models/explanation_generation.py`

## Migration from Notebooks to Code

The original notebooks have been refactored into a modular, production-ready Python package with the following improvements:

### Code Organization
- **Modular Design**: Each notebook's functionality is split into focused modules
- **Separation of Concerns**: Data loading, preprocessing, modeling, and evaluation are separate
- **Reusability**: Functions can be imported and used across different contexts

### Production Readiness
- **Error Handling**: Robust error handling and logging
- **Configuration**: Environment-based configuration management
- **Testing**: Unit tests and integration tests
- **Documentation**: Comprehensive API documentation

### Performance Improvements
- **Batch Processing**: Support for batch inference
- **Caching**: Intelligent caching of preprocessing results
- **Parallelization**: Multi-core processing support
- **Memory Management**: Efficient memory usage patterns

## Running the Original Notebooks

To run the original notebooks:

1. Ensure you have Jupyter installed:
   ```bash
   pip install jupyter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

3. Start Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open any of the `.ipynb` files in this directory

## Comparison with Refactored Code

| Aspect | Original Notebooks | Refactored Code |
|--------|-------------------|-----------------|
| Structure | Monolithic cells | Modular functions/classes |
| Error Handling | Minimal | Comprehensive |
| Testing | None | Unit + Integration tests |
| Configuration | Hardcoded values | Environment-based |
| Logging | Print statements | Structured logging |
| Reusability | Copy-paste | Import and use |
| Production Ready | No | Yes |

## Best Practices for Notebook Development

If you're developing new notebooks, consider these practices:

1. **Keep notebooks focused** on exploration and prototyping
2. **Extract reusable code** into Python modules early
3. **Document your experiments** with markdown cells
4. **Use version control** for notebooks (consider using nbstripout)
5. **Test your code** before moving to production

## Converting Notebooks to Code

For future notebook-to-code migrations, follow this process:

1. **Identify core functions** in the notebook
2. **Extract data processing** into data modules
3. **Create model classes** for ML components  
4. **Build pipeline classes** for orchestration
5. **Add configuration** and error handling
6. **Write tests** for all components
7. **Create examples** showing usage