# ThinkML

ThinkML is a comprehensive machine learning library built on top of scikit-learn, providing advanced validation, feature engineering, and model selection capabilities with robust edge case handling.

> **IMPORTANT**: This library is exclusively available from the author's GitHub account. It is not and will not be available on PyPI or any other package repository. The only official source is: https://github.com/ArpanChaudhary/ThinkML

## Features

### 1. Advanced Validation Methods
- Nested Cross-Validation with enhanced error handling
- Time Series Validation with gap support
- Stratified Group Validation
- Bootstrap Validation with stratification

### 2. Feature Engineering
- Automated feature creation
- Intelligent feature selection
- Support for various feature types:
  - Polynomial features
  - Interaction features
  - Domain-specific features

### 3. Robust Preprocessing
- Advanced scaling with edge case handling
- Support for:
  - Empty datasets
  - Single row datasets
  - Missing data
  - Extreme values
  - Highly correlated features

### 4. Performance
- Efficient handling of large datasets (1M+ rows)
- Memory-optimized validation methods
- Parallel processing support
- Chunked data processing

## Installation

ThinkML is exclusively available from the author's GitHub repository. It is not available on PyPI or any other package repository. Here are the only official installation methods:

### Method 1 (Recommended)
```bash
pip install git+https://github.com/ArpanChaudhary/ThinkML.git
```

### Method 2
```bash
# Clone the repository
git clone https://github.com/ArpanChaudhary/ThinkML.git

# Change to the project directory
cd ThinkML

# Install the package
pip install -e .
```

### Method 3
```bash
# Download the ZIP file from https://github.com/ArpanChaudhary/ThinkML
# Extract the ZIP file
# Navigate to the extracted directory
cd ThinkML

# Install the package
pip install -e .
```

> **Note**: Any other installation method or source is not official and may contain unauthorized modifications. Always install from the official GitHub repository: https://github.com/ArpanChaudhary/ThinkML

## Dependencies

Before installing ThinkML, ensure you have the following dependencies:
- Python 3.6+
- scikit-learn >= 0.24.0
- numpy >= 1.19.0
- pandas >= 1.2.0

You can install these dependencies automatically during ThinkML installation, or manually:
```bash
pip install scikit-learn>=0.24.0 numpy>=1.19.0 pandas>=1.2.0
```

## Quick Start

```python
from thinkml.validation import NestedCrossValidator
from thinkml.feature_engineering import create_features
from sklearn.ensemble import RandomForestClassifier

# Initialize validator
validator = NestedCrossValidator(
    estimator=RandomForestClassifier(),
    param_grid={'n_estimators': [100, 200]},
    inner_cv=3,
    outer_cv=5
)

# Create features and validate
X_new = create_features(X)
results = validator.fit_predict(X_new, y)

print(f"Mean Score: {results['mean_score']:.3f} ± {results['std_score']:.3f}")
```

## Documentation

For detailed documentation, visit our [documentation site](docs/):
- [Implementation Details](docs/implementation_details.md)
- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)

## Requirements

- Python 3.6+
- scikit-learn >= 0.24.0
- numpy >= 1.19.0
- pandas >= 1.2.0

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use ThinkML in your research, please cite:

```bibtex
@software{thinkml2025,
  title = {ThinkML: Advanced Validation and Feature Engineering for Machine Learning},
  author = {Chaudhary, Arpan},
  year = {2025},
  version = {1.0},
  url = {https://github.com/ArpanChaudhary/ThinkML}
}
```

## Acknowledgments

- Thanks to all contributors who have helped shape ThinkML
- Inspired by various open-source machine learning libraries
- Special thanks to the Python data science community

## Contact

Arpan Chaudhary - [@ArpanChaudhary](https://github.com/ArpanChaudhary)

Project Link: [https://github.com/ArpanChaudhary/ThinkML](https://github.com/ArpanChaudhary/ThinkML)

## Support

If you encounter any issues or have questions, please:

1. Check the [documentation](https://github.com/ArpanChaudhary/ThinkML#readme)
2. Search existing [issues](https://github.com/ArpanChaudhary/ThinkML/issues)
3. Create a new issue if needed

## Roadmap

- [ ] Enhanced deep learning support
- [ ] Automated hyperparameter tuning
- [ ] Distributed computing support
- [ ] Model deployment tools
- [ ] Web API interface
- [ ] GUI for interactive model building 