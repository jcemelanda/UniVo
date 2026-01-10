"""GUI implementation for UniVo using BeeWare Toga.

Provides a responsive, cross-platform interface for pictogram-based communication.
Uses a dynamic render loop to switch between Home (categories) and Category views.
"""
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import toga
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

from univo.core.i18n import _, i18n
from univo.core.services import PictogramService

if TYPE_CHECKING:
    from univo.core.domain import Category, Pictogram


class UniVoTogaApp(toga.App):
    """The main Toga application class for UniVo.
    
    Manages navigation state and coordinate widget rendering on the main window.
    """

    def startup(self) -> None:
        self.service = PictogramService()
        # MainWindow might be seen as untyped or returning Union
        self.main_window = cast(Any, toga.MainWindow)(title=_("UniVo"))
        
        # State: None means home (categories list), otherwise category ID
        self.current_category_id: str | None = None
        
        self.main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        self.scroll_container = toga.ScrollContainer(
            horizontal=False, 
            style=Pack(flex=1)
        )
        
        self.render()

        # Ensure main_window is treated as Window and not str
        if self.main_window and not isinstance(self.main_window, str):
            self.main_window.content = self.main_box
            self.main_window.size = (800, 600)
            self.main_window.show()


    def render(self) -> None:
        """The primary render method. 
        
        Clears the main box and rebuilds the UI based on the 
        current_category_id state.
        """
        self.main_box.clear()
        
        # Base path for resources
        base_path = Path(__file__).parent.parent.parent
        
        # --- Fixed Top Bar (Improved Header) ---
        header_box = toga.Box(
            style=Pack(
                direction=ROW, 
                padding=15, 
                background_color="indigo", 
                align_items=CENTER
            )
        )
        
        # App Title in Header
        app_title = toga.Label(
            "UniVo",
            style=Pack(
                color="white", 
                font_size=20, 
                font_weight="bold", 
                margin_right=20
            )
        )
        header_box.add(app_title)

        # Home/Categories Button
        home_btn = toga.Button(
            _("Home"),
            on_press=self.go_home,
            style=Pack(width=100, margin_right=10)
        )
        header_box.add(home_btn)

        # Language Selector
        langs = sorted(i18n.available_languages)
        display_names = {"en": "English", "pt": "Português"}
        selection_items = [display_names.get(code, code.upper()) for code in langs]
        
        self.lang_selection = toga.Selection(
            items=selection_items,
            on_change=self.change_language,
            style=Pack(width=120)
        )
        # Determine current selection
        current_display = display_names.get(
            i18n.current_language, 
            i18n.current_language.upper()
        )
        self.lang_selection.value = current_display
        header_box.add(self.lang_selection)

        # Spacer to push YES/NO further if needed, but in Toga ROW it's sequential
        header_box.add(toga.Box(style=Pack(flex=1)))

        yes_pic = self.service.get_pictogram_by_id("yes")
        yes_btn = toga.Button(
            _("yes"),
            on_press=lambda w: self.create_handler(
                yes_pic
            )(w) if yes_pic else None,
            style=Pack(
                width=80, 
                margin_left=10, 
                background_color="#22c55e", 
                color="white"
            )
        )
        header_box.add(yes_btn)
        
        no_pic = self.service.get_pictogram_by_id("no")
        no_btn = toga.Button(
            _("no"),
            on_press=lambda w: self.create_handler(
                no_pic
            )(w) if no_pic else None,
            style=Pack(
                width=80, 
                margin_left=10, 
                background_color="#ef4444", 
                color="white"
            )
        )
        header_box.add(no_btn)
            
        self.main_box.add(header_box)
        # -------------------------
        # -------------------------

        grid_content = toga.Box(style=Pack(direction=COLUMN))
        
        if self.current_category_id is None:
            # RENDER HOME (List Categories)
            self.render_home(grid_content, base_path)
        else:
            # RENDER CATEGORY (List Pictograms)
            self.render_category(
                grid_content, 
                self.current_category_id, 
                base_path
            )

        self.scroll_container.content = grid_content
        self.main_box.add(self.scroll_container)

    def render_home(self, container: toga.Box, base_path: Path) -> None:
        """Displays all categories as interactive folder-like buttons."""
        title_box = toga.Box(style=Pack(padding=20))
        title = toga.Label(
            _("Categories"), 
            style=Pack(font_size=24, font_weight="bold", color="indigo")
        )
        title_box.add(title)
        self.main_box.add(title_box)
        
        current_row: toga.Box | None = None
        for i, category in enumerate(self.service.categories):
            if i % 4 == 0:
                current_row = toga.Box(style=Pack(direction=ROW, padding=10))
                container.add(current_row)
            
            widget = self.create_category_widget(category)
            if current_row:
                current_row.add(widget)

    def render_category(
        self, 
        container: toga.Box, 
        cat_id: str, 
        base_path: Path
    ) -> None:
        """Displays pictograms belonging to a specific category."""
        category = self.service.get_category_by_id(cat_id)
        if not category:
            self.go_home(None) # Go back to home if category not found
            return

        title_box = toga.Box(style=Pack(padding=20))
        title = toga.Label(
            f"{_('Category')}: {category.name}", 
            style=Pack(font_size=24, font_weight="bold", color="indigo")
        )
        title_box.add(title)
        self.main_box.add(title_box)
        
        current_row: toga.Box | None = None
        for i, pictogram in enumerate(category.pictograms):
            if i % 4 == 0:
                current_row = toga.Box(style=Pack(direction=ROW, padding=10))
                container.add(current_row)
            
            widget = self.create_pictogram_widget(pictogram, base_path)
            if current_row:
                current_row.add(widget)

    def go_home(self, widget: Any) -> None:
        """Navigation handler to return to the category list."""
        self.current_category_id = None
        self.render()

    def create_category_widget(self, category: Category) -> toga.Box:
        """Creates a card-like widget for a category."""
        card = toga.Box(
            style=Pack(
                direction=COLUMN, 
                padding=10, 
                width=160, 
                align_items=CENTER,
                background_color="#f3f4f6"
            )
        )
        
        btn = toga.Button(
            "📂", 
            on_press=lambda w: self.select_category(category.id),
            style=Pack(width=140, height=120, font_size=40)
        )
        card.add(btn)
        
        lbl = toga.Label(
            category.name,
            style=Pack(
                margin_top=10, 
                text_align=CENTER, 
                font_size=14, 
                font_weight="bold",
                color="#374151"
            )
        )
        card.add(lbl)
        
        # Wrap card for outer spacing
        item_box = toga.Box(style=Pack(padding=5))
        item_box.add(card)
        return item_box

    def select_category(self, cat_id: str) -> None:
        """Selection handler for categories."""
        self.current_category_id = cat_id
        self.render()

    def change_language(self, widget: toga.Selection) -> None:
        """Language change handler dynamic to available codes."""
        display_to_code = {
            "English": "en",
            "Português": "pt"
        }
        val = str(widget.value)
        new_lang = display_to_code.get(val, val.lower())
        
        if i18n.current_language != new_lang:
            i18n.load_language(new_lang)
            self.render()


    def create_pictogram_widget(
        self, 
        pictogram: Pictogram, 
        base_path: Path
    ) -> toga.Box:
        """Creates a card-like widget for a pictogram."""
        handler = self.create_handler(pictogram)
        
        card = toga.Box(
            style=Pack(
                direction=COLUMN, 
                padding=10, 
                width=160, 
                align_items=CENTER,
                background_color="white"
            )
        )
        
        # Resolve Icon Path
        icon = None
        if pictogram.image_path:
            full_path = base_path / pictogram.image_path
            if full_path.exists():
                icon = toga.Icon(full_path)
            else:
                print(f"Warning: Icon not found at {full_path}")
        
        # Create Button
        if icon:
            button = toga.Button(
                icon=icon,
                on_press=handler,
                style=Pack(width=140, height=140)
            )
        else:
            button = toga.Button(
                pictogram.label,
                on_press=handler,
                style=Pack(width=140, height=140, font_weight="bold")
            )
        
        card.add(button)
        
        lbl = toga.Label(
            pictogram.label, 
            style=Pack(
                margin_top=10, 
                text_align=CENTER, 
                font_size=12,
                color="#1f2937"
            )
        )
        card.add(lbl)
        
        # Wrap card for outer spacing
        item_box = toga.Box(style=Pack(padding=5))
        item_box.add(card)
        return item_box

    def create_handler(self, pictogram: Pictogram) -> Callable[[Any], Any]:
        """Creates an async handler for pictogram selection.
        
        Eventually this will trigger TTS. Currently shows a dialog.
        """
        async def handler(widget: Any) -> None:
            print(
                f"Pictogram pressed: {pictogram.label}, "
                f"Command: {pictogram.voice_command}"
            )
            # Placeholder for TTS
            if self.main_window and not isinstance(self.main_window, str):
                title = _("Pictogram Selected")
                message = _("You selected: {label}\nVoice: {voice}").format(
                    label=pictogram.label, 
                    voice=pictogram.voice_command
                )
                await self.main_window.dialog(
                    toga.InfoDialog(title, message)
                )

        return handler

