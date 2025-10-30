# 🤝 Contributing to SHIELD

Thank you for your interest in contributing to SHIELD! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Submitting Changes](#submitting-changes)
7. [Style Guidelines](#style-guidelines)

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive environment
- Report unacceptable behavior

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Basic understanding of FastAPI and async Python
- Familiarity with cybersecurity concepts (helpful but not required)

### Areas for Contribution

- 🐛 **Bug Fixes**: Fix reported issues
- ✨ **Features**: Implement new security analysis capabilities
- 📚 **Documentation**: Improve guides and API docs
- 🧪 **Testing**: Add test coverage
- 🎨 **Frontend**: Enhance UI/UX
- 🤖 **ML Models**: Improve threat detection accuracy

## 💻 Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SHIELD.git
   cd SHIELD
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Tests**
   ```bash
   python test_integration.py
   python test_end_to_end.py
   ```

## 🔧 Making Changes

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions

Example:
```bash
git checkout -b feature/add-xss-detection
```

### Commit Messages

Follow conventional commits format:

```
type(scope): brief description

Detailed explanation (optional)

Closes #issue_number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(api): add XSS detection endpoint

Implements real-time XSS attack detection with confidence scoring.
Includes pattern matching and machine learning classification.

Closes #42
```

```
fix(honeypot): correct response timing issue

Fixed race condition in honeypot response generation
that caused intermittent 500 errors.

Closes #38
```

## 🧪 Testing

### Running Tests

```bash
# Integration tests
python backend/test_integration.py

# End-to-end tests
python backend/test_end_to_end.py
```

### Writing Tests

- Add tests for new features
- Ensure existing tests pass
- Aim for meaningful test coverage
- Test edge cases and error conditions

### Test Structure

```python
def test_feature_name():
    """Clear description of what is being tested."""
    # Arrange
    setup_test_data()
    
    # Act
    result = perform_action()
    
    # Assert
    assert result == expected_outcome
```

## 📤 Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README if features change
   - Add comments to complex code
   - Update API documentation

2. **Create Pull Request**
   - Clear title describing the change
   - Detailed description of what and why
   - Reference related issues
   - Include screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   How was this tested?
   
   ## Screenshots (if applicable)
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] All tests passing
   ```

4. **Review Process**
   - Address reviewer feedback
   - Keep PR focused and manageable
   - Update based on suggestions
   - Maintain respectful communication

## 🎨 Style Guidelines

### Python Code Style

- Follow **PEP 8** conventions
- Use **type hints** for function signatures
- Write **docstrings** for classes and functions
- Maximum line length: **88 characters** (Black formatter)

```python
from typing import Optional, Dict, List

async def analyze_threat(
    input_text: str,
    analysis_type: str = "sql_injection"
) -> Dict[str, any]:
    """
    Analyze input for security threats.
    
    Args:
        input_text: Text to analyze
        analysis_type: Type of analysis to perform
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If analysis_type is invalid
    """
    # Implementation
    pass
```

### JavaScript Code Style

- Use **ES6+** syntax
- Consistent indentation (4 spaces)
- Descriptive variable names
- Add comments for complex logic

```javascript
class ThreatAnalyzer {
    constructor(config) {
        this.apiUrl = config.apiUrl;
        this.timeout = config.timeout || 5000;
    }
    
    async analyzeThreat(inputData) {
        // Clear description of complex logic
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                body: JSON.stringify(inputData)
            });
            return await response.json();
        } catch (error) {
            console.error('Analysis failed:', error);
            throw error;
        }
    }
}
```

### HTML/CSS Style

- Semantic HTML5 elements
- BEM naming convention for CSS
- Mobile-first responsive design
- Accessibility considerations (ARIA labels, alt text)

## 📁 File Organization

- Backend code in `/backend/app/`
- Frontend code in `/web/`
- Tests alongside implementation
- Documentation in `/docs/`
- Assets in `/assets/`

## 🔒 Security Considerations

- Never commit sensitive data (API keys, passwords)
- Use `.env` for configuration
- Validate all user inputs
- Follow OWASP security guidelines
- Report security vulnerabilities privately

## 📞 Getting Help

- Check existing issues and discussions
- Review documentation in `/docs/`
- Ask questions in GitHub Discussions
- Join project communication channels

## 🎯 Priority Areas

Current focus areas for contributions:

1. **ML Model Improvements** - Enhance detection accuracy
2. **Honeypot Enhancement** - More realistic deception
3. **Frontend Polish** - UI/UX improvements
4. **Test Coverage** - Increase test coverage
5. **Documentation** - Expand guides and examples

## 🙏 Thank You!

Your contributions help make SHIELD better for everyone. We appreciate your time and effort!

---

**Questions?** Open an issue or start a discussion. We're here to help! 🚀
