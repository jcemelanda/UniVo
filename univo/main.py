import argparse

from univo.ui.toga.app import UniVoTogaApp
from univo.ui.tui.app import UniVoTUIApp


def main() -> None:
    """Parses arguments and starts the selected user interface."""
    parser = argparse.ArgumentParser(description="UniVo - AAC Application")
    parser.add_argument(
        "--ui",
        choices=["toga", "tui"],
        default="toga",
        help="Choose UI interface (default: toga)"
    )
    args = parser.parse_args()

    if args.ui == "toga":
        # Toga app instantiation
        app = UniVoTogaApp("UniVo", "org.univo.app")
        app.main_loop()
    else:
        # Textual TUI app instantiation
        tui_app = UniVoTUIApp()
        tui_app.run()


if __name__ == '__main__':
    main()
