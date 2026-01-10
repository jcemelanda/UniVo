"""Terminal User Interface for UniVo using Textual.

Provides a fast, keyboard-friendly interface for communication in the terminal.
Uses a reactive component model to re-render the main view upon navigation.
"""
from textual.app import App, ComposeResult
from textual.containers import Horizontal, ScrollableContainer
from textual.widgets import Button, Footer, Header, Static

from univo.core.i18n import _, i18n
from univo.core.services import PictogramService


class UniVoTUIApp(App[None]):
    """The main Textual application class for UniVo.
    
    Manages terminal-based layouts, CSS styles, and navigation state.
    """

    
    CSS = """
    #fixed-bar {
        dock: top;
        height: 5;
        background: $primary-darken-2;
        content-align: center middle;
        padding: 1;
    }
    #main-container {
        padding: 1;
    }
    .grid {
        layout: grid;
        grid-size: 3;
        grid-gutter: 1 2;
    }
    Button {
        width: 100%;
    }
    #btn-home {
        background: $accent;
        color: $text;
    }
    #btn-yes {
        background: green;
        color: white;
    }
    #btn-no {
        background: red;
        color: white;
    }
    .category-btn {
        border: tall $secondary;
        background: $secondary-darken-2;
    }
    .title {
        text-align: center;
        text-style: bold;
        background: $boost;
        padding: 1;
    }

    """
    
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"), 
        ("l", "toggle_language", "Toggle Language"),
        ("q", "quit", "Quit")
    ]

    def __init__(self) -> None:
        super().__init__()
        self.service = PictogramService()
        self.current_category_id: str | None = None

    def compose(self) -> ComposeResult:
        """Defines the initial layout of the application."""
        yield Header()
        with Horizontal(id="fixed-bar"):
            yield Button(_("Home"), id="btn-home")
            yield Button(_("yes"), id="btn-yes", variant="success")
            yield Button(_("no"), id="btn-no", variant="error")
            
        with ScrollableContainer(id="main-container"):
            yield from self.render_content()
        yield Footer()

    def render_content(self) -> ComposeResult:
        """Renders the dynamic part of the UI (Home or Category)."""
        if self.current_category_id is None:
            # Home View
            yield Static(_("Categories"), classes="title")

            yield Horizontal(
                *[
                    Button(
                        f"📂 {category.name}", 
                        id=f"cat-{category.id}",
                        classes="category-btn"
                    ) for category in self.service.categories
                ],
                classes="grid"
            )

        else:
            # Category View
            cat_id = self.current_category_id
            category_obj = self.service.get_category_by_id(cat_id)
            if category_obj:
                yield Static(f"{_('Category')}: {category_obj.name}", classes="title")
                yield Horizontal(
                    *[
                        Button(pictogram.label, id=f"btn-{pictogram.id}")
                        for pictogram in category_obj.pictograms
                    ],
                    classes="grid"
                )




    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Global button click handler for navigation and selection."""
        button_id = event.button.id
        if not button_id:
            return

        if button_id == "btn-home":
            self.current_category_id = None
            await self.refresh_view()
        elif button_id.startswith("cat-"):
            self.current_category_id = button_id.replace("cat-", "")
            await self.refresh_view()
        elif button_id == "btn-yes":
            self.notify(_("Selected: {label}").format(label=_("yes")))
        elif button_id == "btn-no":
            self.notify(_("Selected: {label}").format(label=_("no")))
        elif button_id.startswith("btn-"):
            pic_id = button_id.replace("btn-", "")
            pictogram = self.service.get_pictogram_by_id(pic_id)
            if pictogram:
                self.notify(_("Selected: {label}").format(label=pictogram.label))

    async def refresh_view(self) -> None:
        """Clears the main container and re-mounts the current content."""
        container = self.query_one("#main-container")
        # Remove all widgets inside the container
        for child in list(container.children):
            await child.remove()
        
        # Mount new content
        await container.mount_all(list(self.render_content()))

    def action_toggle_language(self) -> None:
        """Action handler for the 'L' hotkey to cycle through all languages."""
        langs = sorted(i18n.available_languages)
        if not langs:
            return
            
        try:
            current_index = langs.index(i18n.current_language)
            next_index = (current_index + 1) % len(langs)
        except ValueError:
            next_index = 0
            
        new_lang = langs[next_index]
        i18n.load_language(new_lang)
        self.call_after_refresh(self.refresh_view)
        # Translating the notification itself is good practice
        msg = f"Language: {new_lang.upper()}"
        self.notify(msg)


if __name__ == "__main__":
    app = UniVoTUIApp()
    app.run()
