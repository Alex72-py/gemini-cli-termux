# Contributing to Gemini CLI for Termux

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Alex72-py/gemini-cli-termux/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Termux version and Android version
   - Error messages or logs

### Suggesting Features

1. Check [existing feature requests](https://github.com/Alex72-py/gemini-cli-termux/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue describing:
   - The feature and its use case
   - How it would work
   - Why it would be valuable

### Contributing Code

1. **Fork the repository**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/gemini-cli-termux.git
   cd gemini-cli-termux
   ```

2. **Create a feature branch**
   
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Install development dependencies**
   
   ```bash
   pip install --break-system-packages -e ".[dev]"
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add docstrings to functions/classes
   - Update documentation if needed

5. **Test your changes**
   
   ```bash
   # Run tests
   python -m pytest tests/
   
   # Format code
   python -m black gemini_cli/
   python -m isort gemini_cli/
   
   # Check for issues
   python -m flake8 gemini_cli/
   ```

6. **Commit your changes**
   
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```
   
   Use clear commit messages:
   - `feat: Add new feature`
   - `fix: Fix bug in X`
   - `docs: Update documentation`
   - `refactor: Refactor code`
   - `test: Add tests`

7. **Push to your fork**
   
   ```bash
   git push origin feature/amazing-feature
   ```

8. **Open a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Describe your changes clearly
   - Link any related issues

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Keep functions focused and small
- Write descriptive variable names

### Documentation

- Add docstrings to all public functions/classes
- Update README.md if adding features
- Comment complex logic

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test on actual Termux if possible

### Termux-Specific Considerations

- Always use Termux-compatible paths
- Test clipboard integration with Termux-API
- Ensure no native dependencies are added
- Verify Python-only solutions work

## Questions?

Feel free to:
- Open an issue for discussion
- Join discussions in existing issues
- Ask questions in Pull Requests

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the code, not the person
- Help make this project better for everyone

Thank you for contributing! 🚀
