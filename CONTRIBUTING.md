# Contributing to LifeUnity AI — Cognitive Twin System

Thank you for your interest in contributing to LifeUnity AI! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a positive environment

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples or mockups

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin.git
   cd lifeunity-ai-cognitive-twin
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed
   - Ensure code is well-tested

4. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Include screenshots for UI changes

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin.git
   cd lifeunity-ai-cognitive-twin
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Maximum line length: 100 characters

## Testing

Before submitting a PR:
- Test your changes thoroughly
- Ensure existing functionality still works
- Test on different screen sizes (for UI changes)
- Run the import test: `python test_modules.py`

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions/classes
- Update type hints where applicable
- Include usage examples for new features

## Areas for Contribution

### High Priority
- Additional emotion detection models
- Real-time webcam streaming
- Export functionality for reports
- Mobile-responsive UI improvements
- Performance optimizations

### Medium Priority
- Multi-language support
- Voice emotion detection
- Integration with wearables
- Advanced data visualizations
- User authentication system

### Good First Issues
- UI/UX improvements
- Documentation enhancements
- Bug fixes
- Test coverage
- Code cleanup

## Questions?

Feel free to:
- Open an issue for discussion
- Reach out to the maintainers
- Join community discussions

Thank you for contributing to LifeUnity AI! 🧠💙
