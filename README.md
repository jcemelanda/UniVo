# UniVo - Augmentative and Alternative Communication (AAC)

**UniVo** is a free, open-source communication tool designed to be accessible on every platform. It uses pictograms and text-to-speech (TTS) to empower individuals with communication disabilities.

> 💡 **Communication is a right, not a privilege.**

---

## 🌍 Key Features
- **Multi-Platform**: Runs on Desktop (Linux, macOS, Windows), Mobile (Android, iOS), and even the Terminal (TUI).
- **Category-Based Navigation**: Organize pictograms into folders for quick access.
- **Fixed Responses**: Persistent "Home", "Yes", and "No" buttons for essential communication.
- **Dynamic Seeding**: Automatically loads pictograms from the `resources` directory.

---

## 🛠️ Architecture
UniVo is built with a **decoupled architecture**, separating the core domain logic from the user interface:

- **Core Layer**: 
  - `domain.py`: Entities (Pictogram, Category) using Fluent Python patterns.
  - `database.py`: SQLite persistence and automatic seeding.
  - `services.py`: High-level business logic and coordinate between UI and DB.
- **UI Layer**:
  - `ui/toga/`: Graphical interface using BeeWare Toga.
  - `ui/tui/`: Terminal interface using Textual.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- `pip`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/UniVo.git
   cd UniVo
   ```
2. Install dependencies:
   ```bash
   pip install -e .
   ```

### Running the App
- **GUI (Toga)**:
  ```bash
  python -m univo.main
  ```
- **TUI (Terminal)**:
  ```bash
  python -m univo.main --ui tui
  ```

---

## 👩‍💻 Development

### Quality Standards
We enforce strict coding standards using `ruff` and `mypy`:
```bash
ruff check .
mypy .
pytest
```

---

## 🤝 Contributing
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to help improve UniVo.

## 📄 License
This project is open-source and free for everyone.