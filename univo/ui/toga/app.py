"""GUI implementation for UniVo using BeeWare Toga.

Provides a responsive, cross-platform interface for pictogram-based communication.
Uses a dynamic render loop to switch between Home (categories) and Category views.
"""
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import toga
from toga.style import Pack

# mypy doesn't see these exports easily in some toga versions
from toga.style.pack import CENTER, COLUMN, ROW  # type: ignore

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
        self.main_window = cast(Any, toga.MainWindow)(title=self.formal_name)
        
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
            self.main_window.show()


    def render(self) -> None:
        """The primary render method. 
        
        Clears the main box and rebuilds the UI based on the 
        current_category_id state.
        """
        self.main_box.clear()
        
        # Base path for resources
        base_path = Path(__file__).parent.parent.parent
        
        # --- Fixed Top Bar (Always Present) ---
        fixed_box = toga.Box(
            style=Pack(direction=ROW, margin_bottom=10, align_items=CENTER)
        )
        
        # Home/Categories Button
        home_btn = toga.Button(
            "🏠 Home",
            on_press=self.go_home,
            style=Pack(width=100, margin_right=10)
        )
        fixed_box.add(home_btn)

        yes_pic = self.service.get_pictogram_by_id("yes")
        if yes_pic:
            fixed_box.add(self.create_pictogram_widget(yes_pic, base_path))
            
        fixed_box.add(toga.Box(style=Pack(width=10)))
        
        no_pic = self.service.get_pictogram_by_id("no")
        if no_pic:
            fixed_box.add(self.create_pictogram_widget(no_pic, base_path))
            
        self.main_box.add(fixed_box)
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
        title = toga.Label(
            "Categories", 
            style=Pack(margin_bottom=10, font_size=16, font_weight="bold")
        )
        self.main_box.add(title)
        
        current_row: toga.Box | None = None
        for i, category in enumerate(self.service.categories):
            if i % 3 == 0:
                current_row = toga.Box(style=Pack(direction=ROW, margin=5))
                container.add(current_row)
            
            # Categories are rendered as special buttons
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

        title = toga.Label(
            f"Category: {category.name}", 
            style=Pack(margin_bottom=10, font_size=16, font_weight="bold")
        )
        self.main_box.add(title)
        
        current_row: toga.Box | None = None
        for i, pictogram in enumerate(category.pictograms):
            if i % 3 == 0:
                current_row = toga.Box(style=Pack(direction=ROW, margin=5))
                container.add(current_row)
            
            widget = self.create_pictogram_widget(pictogram, base_path)
            if current_row:
                current_row.add(widget)

    def go_home(self, widget: Any) -> None:
        """Navigation handler to return to the category list."""
        self.current_category_id = None
        self.render()

    def create_category_widget(self, category: Category) -> toga.Box:
        """Creates a composite widget for a category.
        
        Displays a folder icon button and a label below it.
        """
        item_box = toga.Box(
            style=Pack(direction=COLUMN, margin=5, width=120, align_items=CENTER)
        )
        
        btn = toga.Button(
            "📂", # Using folder emoji for simplicity
            on_press=lambda w: self.select_category(category.id),
            style=Pack(width=100, height=80, font_size=30)
        )
        item_box.add(btn)
        
        lbl = toga.Label(
            category.name,
            style=Pack(
                margin_top=5, 
                text_align=CENTER, 
                font_size=12, 
                font_weight="bold"
            )
        )

        item_box.add(lbl)
        return item_box

    def select_category(self, cat_id: str) -> None:
        """Selection handler for categories."""
        self.current_category_id = cat_id
        self.render()


    def create_pictogram_widget(
        self, 
        pictogram: Pictogram, 
        base_path: Path
    ) -> toga.Box:
        """Creates a composite widget for a pictogram.
        
        Displays the image icon (or label fallback) and a text label below.
        """
        handler = self.create_handler(pictogram)
        
        # Container for each item (Button + Label)
        item_box = toga.Box(
            style=Pack(direction=COLUMN, margin=5, width=120, align_items=CENTER)
        )
        
        # Resolve Icon Path
        icon = None
        if pictogram.image_path:
            full_path = base_path / pictogram.image_path
            if full_path.exists():
                icon = toga.Icon(full_path)
            else:
                print(f"Warning: Icon not found at {full_path}")
        
        # Create Button (Icon OR Text, not both)
        if icon:
            # Icon button (no text)
            button = toga.Button(
                icon=icon,
                on_press=handler,
                style=Pack(width=100, height=100)
            )
        else:
            # Text fallback button
            button = toga.Button(
                pictogram.label,
                on_press=handler,
                style=Pack(width=100, height=100)
            )
        
        item_box.add(button)
        
        # Label below the button
        lbl = toga.Label(
            pictogram.label, 
            style=Pack(margin_top=5, text_align=CENTER, font_size=10)
        )
        item_box.add(lbl)
        
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
                await self.main_window.dialog(
                    toga.InfoDialog(
                        "Pictogram Selected", 
                        f"You selected: {pictogram.label}\n"
                        f"Voice: {pictogram.voice_command}"
                    )
                )

        return handler

