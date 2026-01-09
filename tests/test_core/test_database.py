from pathlib import Path

import pytest

from univo.core.database import DatabaseManager


@pytest.fixture
def db_path(tmp_path: Path) -> str:
    # Setup: Create a temporary database file
    return str(tmp_path / "test_univo.db")

@pytest.fixture
def db_manager(db_path: str) -> DatabaseManager:
    # Initialize DatabaseManager with temp path
    # This should trigger schema creation and seeding
    return DatabaseManager(db_path=db_path)

def test_db_init(db_manager: DatabaseManager) -> None:
    """Verify that database is created and seeded."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Check categories
        cursor.execute("SELECT count(*) FROM categories")
        count = cursor.fetchone()[0]
        assert count > 0, "Categories should be seeded"
        
        # Check main/actions category exists (depending on seed logic)
        # The seed logic currently scans resources, but if resources 
        # aren't found relative to the temporary test file location??
        # Wait, the seed logic uses `Path(__file__).parent.parent` 
        # inside `core/database.py`. 
        # `__file__` is the installed package location or source location.

        # It should still find the resources if the project structure is intact.
        pass

def test_schema_existence(db_manager: DatabaseManager) -> None:
    """Verify tables exist."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        assert "categories" in tables
        assert "pictograms" in tables

def test_seed_consistency(db_manager: DatabaseManager) -> None:
    """Verify that we have some known data if seeding worked."""
    # Since seeding depends on the environment resources, 
    # we might ideally mock the resource scan,
    # but for an integration test of the DB layer, 
    # checking 'count > 0' is a good sanity check.
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        assert count > 0

def test_manual_insert(db_manager: DatabaseManager) -> None:
    """Test manual data insertion."""
    test_id = "test_cat"
    test_name = "Test Category"
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (id, name) VALUES (?, ?)", 
            (test_id, test_name)
        )
        conn.commit()

        
        cursor.execute("SELECT * FROM categories WHERE id = 'test_cat'")
        row = cursor.fetchone()
        assert row['name'] == "Test Category"
