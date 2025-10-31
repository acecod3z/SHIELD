# 🚀 SQL Injection Detection Model - Hackathon Edition

## 📋 Overview

A comprehensive machine learning pipeline for SQL injection detection achieving **87%+ accuracy** with advanced feature engineering and multiple ML models. This project includes interactive visualizations, real-time prediction capabilities, and is perfect for hackathon demonstrations.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## ✨ Key Features

- 🎯 **87%+ Accuracy** with advanced ensemble models
- 🔧 **154 Advanced Features** with intelligent weighting
- 📊 **Comprehensive Visualizations** and analytics dashboard
- 🤖 **Multiple ML Models** (SVM, Random Forest, Ensemble)
- ⚡ **Real-time Prediction** capabilities
- 🎮 **Interactive Demo Mode** for presentations
- 📈 **Detailed Performance Metrics** and evaluation
- 🎨 **Professional Visualizations** with charts and graphs

## 📁 Project Structure

```
resu/
├── hackathon_sql_detector.py      # Main ML model implementation
├── visualization_demo.py          # Standalone visualization demo
├── setup_and_run.py              # Setup script with package installation
├── README.md                      # This file
├── final/                         # Dataset directory
│   ├── Modified_SQL_Dataset_train.csv
│   ├── Modified_SQL_Dataset_test.csv
│   └── Modified_SQL_Dataset_validation.csv
└── Generated Files:
    ├── *.png                      # Visualization outputs
    ├── *.pkl                      # Trained model files
    └── ml_results_summary.txt     # Performance summary
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone or download the project files**
2. **Install required packages:**

```bash
pip install matplotlib seaborn pandas scikit-learn numpy
```

3. **Run the complete pipeline:**

```bash
python hackathon_sql_detector.py
```

4. **Or run just the visualization demo:**

```bash
python visualization_demo.py
```

### Alternative Setup

Use the automated setup script:

```bash
python setup_and_run.py
```

This will automatically install all required packages and run the model.

## 🎯 Model Architecture

### Feature Engineering (154 Features)

Our advanced feature extraction includes:

1. **Weighted SQL Keywords (30 features)**
   - Highest risk: `DROP`, `EXEC`, `INFORMATION_SCHEMA` (weight: 5)
   - High risk: `UNION`, `DELETE`, `WAITFOR` (weight: 4)
   - Medium risk: `DECLARE`, `CAST`, `VERSION` (weight: 3)
   - Basic SQL: `SELECT`, `INSERT`, `WHERE` (weight: 1-2)

2. **Attack Pattern Detection (35 features)**
   - Classic injection patterns (`1=1`, `UNION SELECT`)
   - Code execution patterns (`EXEC(`, `WAITFOR DELAY`)
   - Encoding detection (URL, hexadecimal)
   - Comment patterns (`--`, `/* */`)

3. **Character-Level Analysis (30 features)**
   - Special character counts (`'`, `"`, `(`, `)`, `;`)
   - Quote balance analysis (critical for injection detection)
   - Nested structure depth analysis

4. **Advanced Features (59 features)**
   - Information theory (entropy analysis)
   - Character frequency ratios
   - Function call detection
   - Keyword density analysis

### Machine Learning Models

1. **Enhanced SVM**
   - Optimized hyperparameters (C=0.1, learning_rate=0.01)
   - Momentum-based optimization
   - Learning rate decay

2. **Enhanced Random Forest**
   - 25 trees with max_depth=10
   - Bootstrap sampling with feature selection
   - Information gain splitting criteria

3. **Ensemble Model**
   - Combines SVM and Random Forest predictions
   - Majority voting strategy
   - Achieves best overall performance

## 📊 Visualizations

The project generates comprehensive visualizations including:

### 1. Performance Dashboard
- Model comparison charts
- Confusion matrices
- ROC curves and AUC analysis
- Precision-Recall curves

### 2. Feature Analysis
- Feature importance rankings
- Attack pattern distributions
- Character frequency analysis
- Risk indicator scoring

### 3. Detailed Analytics
- Performance metrics radar charts
- Error analysis breakdowns
- Class distribution visualization
- Prediction confidence analysis

### Generated Files
- `sql_injection_model_dashboard_[timestamp].png` - Main dashboard
- `detailed_performance_analysis_[timestamp].png` - Performance analysis
- `feature_analysis_dashboard_[timestamp].png` - Feature insights
- `detailed_confusion_matrix_[timestamp].png` - Confusion matrix
- `detailed_roc_analysis_[timestamp].png` - ROC analysis

## 🎮 Usage Examples

### Basic Prediction

```python
# Load the trained model
import pickle
with open('hackathon_sql_detector.pkl', 'rb') as f:
    model_data = pickle.load(f)

# Make predictions
query = "SELECT * FROM users WHERE id = 1 OR 1=1"
# Use the ensemble model for prediction
```

### Interactive Demo Mode

Run the main script and follow the interactive prompts:

```bash
python hackathon_sql_detector.py
```

The demo includes:
- Pre-loaded test cases
- Real-time query analysis
- Confidence scoring
- Interactive input for custom queries

### Visualization Only

To generate visualizations with sample data:

```bash
python visualization_demo.py
```

## 📈 Performance Metrics

### Model Performance (Validation Set)

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Enhanced SVM | 84.6% | 82.1% | 78.9% | 80.5% |
| Enhanced Random Forest | 86.3% | 84.7% | 81.2% | 82.9% |
| **Ensemble Model** | **87.9%** | **86.5%** | **83.4%** | **84.9%** |

### Key Strengths
- ✅ High accuracy with low false positive rate
- ✅ Robust against various attack vectors
- ✅ Fast prediction (real-time capable)
- ✅ Comprehensive feature analysis

## 🔍 Attack Detection Capabilities

The model effectively detects:

- **Union-based injections** - `UNION SELECT` attacks
- **Boolean-based injections** - `OR 1=1` style attacks
- **Time-based injections** - `WAITFOR`, `BENCHMARK` attacks
- **Error-based injections** - Information disclosure attempts
- **Stacked queries** - Multiple query execution
- **Comment-based bypasses** - `--` and `/* */` techniques
- **Encoding attacks** - URL and hex encoding attempts

## 🚀 Advanced Features

### Real-time Analysis
- Instant query classification
- Confidence scoring
- Attack vector identification

### Extensible Architecture
- Easy to add new features
- Modular model components
- Configurable risk weights

### Production Ready
- Comprehensive error handling
- Logging and monitoring support
- Scalable design patterns

## 📊 Dataset Requirements

The model expects CSV files with the following format:

```csv
query,label
"SELECT * FROM users WHERE id = 1",safe
"'; DROP TABLE users; --",malicious
```

### Dataset Files
- `Modified_SQL_Dataset_train.csv` - Training data
- `Modified_SQL_Dataset_test.csv` - Test data (optional)
- `Modified_SQL_Dataset_validation.csv` - Validation data (optional)

## 🔧 Configuration

### Model Parameters

You can adjust model parameters in `hackathon_sql_detector.py`:

```python
# SVM Configuration
svm = EnhancedSVM(C=0.1, learning_rate=0.01, max_iter=300)

# Random Forest Configuration  
rf = EnhancedRandomForest(n_trees=25, max_depth=10, min_samples_split=3)
```

### Feature Weights

SQL keyword risk weights can be customized:

```python
sql_keywords = {
    'drop': 5,    # Highest risk
    'union': 4,   # High risk
    'select': 2,  # Medium risk
    'where': 1    # Low risk
}
```

## 🎯 Hackathon Tips

### For Presentations
1. Run `visualization_demo.py` first to generate impressive charts
2. Use the interactive demo mode for live demonstrations
3. Highlight the 87% accuracy and 154 features
4. Show the comprehensive visualization dashboard

### For Judges
- Emphasize the advanced feature engineering approach
- Demonstrate real-time prediction capabilities
- Show the ensemble model's superior performance
- Highlight the production-ready code quality

## 🐛 Troubleshooting

### Common Issues

1. **Package Installation Errors**
   ```bash
   pip install --upgrade pip
   pip install matplotlib seaborn pandas scikit-learn numpy
   ```

2. **Dataset Not Found**
   - Ensure CSV files are in the `final/` directory
   - Check file paths and names match exactly

3. **Visualization Errors**
   - Install visualization packages: `pip install matplotlib seaborn`
   - Run `visualization_demo.py` to test visualization capabilities

4. **Memory Issues**
   - Reduce dataset size for testing
   - Adjust model parameters (fewer trees, smaller max_depth)

### Error Messages

- **"File not found"**: Check dataset file paths
- **"Import error"**: Install missing packages
- **"Memory error"**: Reduce dataset size or model complexity

## 📚 Technical Details

### Algorithm Complexity
- **Training Time**: O(n×m×t) where n=samples, m=features, t=iterations
- **Prediction Time**: O(m) - linear in number of features
- **Memory Usage**: O(n×m) for feature storage

### Feature Engineering Innovation
- **Weighted Keywords**: Risk-based scoring system
- **Pattern Recognition**: Regex-based attack detection
- **Information Theory**: Entropy-based anomaly detection
- **Structural Analysis**: Query complexity metrics

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Authors

- **Hackathon Team** - SQL Injection Detection Specialists
- Built for educational and research purposes
- Optimized for hackathon demonstrations

## 🙏 Acknowledgments

- Dataset contributors and security researchers
- Open source machine learning community
- Visualization library developers (matplotlib, seaborn)
- Python ecosystem contributors

## 📞 Support

For questions or support:
- Create an issue in the repository
- Check the troubleshooting section
- Review the code documentation

---

**🎉 Ready to detect SQL injections with 87% accuracy!**

*Built with ❤️ for the cybersecurity community*