"""Persistence layer for UniVo using SQLite.

Handles schema initialization, connection management via context managers,
and automatic seeding from the resources directory.
"""
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database interactions.
    
    Ensures tables exist and seeds them from folder structures on startup.
    """
    def __init__(self, db_path: str | None = None) -> None:
        """Initialize database manager.
        
        Args:
            db_path: Absolute path to the .db file. 
                     Overrides default 'univo.db' in project root.
        """
        if db_path is None:
            # univo/core/database.py -> univo/core -> univo -> univo/
            base_dir = Path(__file__).parent.parent
            self.db_path = str(base_dir / "univo.db")
        else:
            self.db_path = db_path
            
        self._init_db()

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection]:
        """Context manager for database connection.
        
        Configures the connection to use sqlite3.Row for dict-like access.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initialize the database schema if tables don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )
            """)
            
            # Create pictograms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pictograms (
                    id TEXT PRIMARY KEY,
                    category_id TEXT NOT NULL,
                    label TEXT NOT NULL,
                    voice_command TEXT,
                    icon_path TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            """)
            
            conn.commit()
            
            # Seed initial data if empty
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                self._seed_data(conn)


    def _seed_data(self, conn: sqlite3.Connection) -> None:
        """Seed initial data from resources directory."""
        cursor = conn.cursor()
        
        # Path to resources/pictograms
        base_dir = Path(__file__).parent.parent
        resources_dir = base_dir / "resources" / "pictograms"
        
        if not resources_dir.exists():
            print(f"Warning: Resources directory not found at {resources_dir}")
            return


        # Iterate over directories (Categories)
        for category_path in resources_dir.iterdir():
            if category_path.is_dir():
                cat_id = category_path.name
                cat_name = category_path.name.capitalize()
                
                cursor.execute(
                    "INSERT INTO categories (id, name) VALUES (?, ?)", 
                    (cat_id, cat_name)
                )
                
                # Iterate over files (Pictograms)
                for file_path in category_path.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in [
                        '.png', '.jpg', '.jpeg'
                    ]:
                        # id = filename without extension
                        pic_id = file_path.stem
                        # label = filename capitalized (replace _ with space)
                        label = pic_id.replace("_", " ").capitalize()
                        voice = label
                        
                        # Store relative path for now
                        icon_rel_path = (
                            f"resources/pictograms/{cat_id}/{file_path.name}"
                        )
                        
                        cursor.execute(
                            "INSERT INTO pictograms "
                            "(id, category_id, label, voice_command, icon_path) "
                            "VALUES (?, ?, ?, ?, ?)",
                            (pic_id, cat_id, label, voice, icon_rel_path)
                        )
        
        conn.commit()
