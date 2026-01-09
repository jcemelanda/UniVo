"""Domain services for UniVo.

Coordinates interactions between the UI and the persistence layer, 
applying business rules and modern Pythonic patterns.
"""
from collections.abc import Iterator
from typing import Any

from .database import DatabaseManager
from .decorators import log_interaction
from .domain import Category, Pictogram
from .interfaces import PictogramRepository


class PictogramService:
    """Orchestrates pictogram and category logic.
    
    Provides high-level access to domain entities using generators,
    properties, and the mapping protocol.
    """
    def __init__(self, db_manager: PictogramRepository | None = None) -> None:
        """Initialize the service with a repository.
        
        Args:
            db_manager: A repository implementation. 
                        Defaults to DatabaseManager.
        """
        self.db: PictogramRepository = db_manager or DatabaseManager()

    @property
    @log_interaction
    def default_category(self) -> Category:
        """Fetch the default (first found) category for initial app view."""
        try:
            return next(self.categories)
        except StopIteration:
            return Category(id="error", name="No Categories Found", pictograms=[])


    @property
    def categories(self) -> Iterator[Category]:
        """Generator that yields all categories with their pictograms.
        
        Lazy-loads pictograms for each category during iteration.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories")
            cat_rows: list[Any] = cursor.fetchall()
            
            for cat_row in cat_rows:
                cat_id: str = cat_row["id"]
                # Fetch pictograms for this category
                cursor.execute(
                    "SELECT * FROM pictograms WHERE category_id = ?", 
                    (cat_id,)
                )
                pic_rows: list[Any] = cursor.fetchall()
                
                pictograms: list[Pictogram] = [
                    Pictogram(
                        id=row["id"],
                        label=row["label"],
                        voice_command=row["voice_command"],
                        image_path=row["icon_path"]
                    ) for row in pic_rows
                ]
                
                yield Category(id=cat_id, name=cat_row["name"], pictograms=pictograms)

    def get_main_category(self) -> Category:
        """Deprecated: Use default_category property instead."""
        return self.default_category

    @log_interaction
    def get_category_by_id(self, category_id: str) -> Category | None:
        """Fetch a specific category and its pictograms by ID."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            cat_row = cursor.fetchone()
            
            if not cat_row:
                return None
                
            cursor.execute(
                "SELECT * FROM pictograms WHERE category_id = ?", 
                (category_id,)
            )
            pic_rows = cursor.fetchall()
            
            pictograms = [
                Pictogram(
                    id=row["id"],
                    label=row["label"],
                    voice_command=row["voice_command"],
                    image_path=row["icon_path"]
                ) for row in pic_rows
            ]
            
            return Category(
                id=cat_row["id"], 
                name=cat_row["name"], 
                pictograms=pictograms
            )

    @log_interaction
    def __getitem__(self, pictogram_id: str) -> Pictogram | None:
        """Finds a pictogram by ID (Mapping protocol: service['id'])."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pictograms WHERE id = ?", (pictogram_id,))
            row: Any | None = cursor.fetchone()

            
            if row:
                return Pictogram(
                    id=row["id"],
                    label=row["label"],
                    voice_command=row["voice_command"],
                    image_path=row["icon_path"]
                )
            return None


    def get_pictogram_by_id(self, pictogram_id: str) -> Pictogram | None:
        """Deprecated: Use service[id] instead."""
        return self[pictogram_id]

    def __iter__(self) -> Iterator[Category]:
        """Iterate over all categories (Iterable protocol)."""
        return self.categories

