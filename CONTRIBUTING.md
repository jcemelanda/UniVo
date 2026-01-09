# Contributing to UniVo

Thank you for considering contributing to UniVo! Together, we can make inclusive communication accessible to everyone.

## 💻 Technical Philosophy
UniVo embraces **Fluent Python** principles:
- Use of magic methods for intuitive sequences and mappings.
- Clean, type-hinted code (checked by `mypy`).
- Modern formatting and linting (enforced by `ruff`).
- Decoupled architecture to support any UI frontend.

## 🛠️ Development Workflow

### Setup
1. Fork the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests
All contributions must pass existing tests and include new ones for new features:
```bash
pytest
```

### Static Analysis
We strictly follow `ruff` and `mypy` (strict mode) rules. Ensure your code passes before submitting a PR:
```bash
# Linting & Formatting
ruff check .
ruff format .

# Type Checking
mypy .
```

## 📝 Pull Request Process
1. Create a new branch for your feature or bugfix.
2. Ensure all tests and static analysis pass.
3. Update documentation if you've added new features or changed behaviors.
4. Open a Pull Request with a clear description of the change.

## 🎨 Design Guidelines
When adding to the UI (Toga or Textual):
- Keep layouts simple and high-contrast for accessibility.
- Ensure consistent iconography and emoji usage.
- Always provide text fallbacks for images.

## 📂 Project Structure
- `univo/core/`: Domain models, database logic, and services.
- `univo/ui/`: UI implementations.
- `resources/`: Pictograms and assets.
- `tests/`: Unit and integration tests.

Thank you for helping us build a more inclusive world!
