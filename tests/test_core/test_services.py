from pathlib import Path  # Added import

import pytest

from univo.core.database import DatabaseManager
from univo.core.services import PictogramService


@pytest.fixture
def db_path(tmp_path: Path) -> str:
    return str(tmp_path / "test_univo.db")

@pytest.fixture
def db_manager(db_path: str) -> DatabaseManager:
    mgr = DatabaseManager(db_path) # Changed db_path=db_path to db_path
    # Clear auto-seeded data to ensure test data is clean
    with mgr.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pictograms")
        cursor.execute("DELETE FROM categories")
        cursor.execute(
            "INSERT INTO categories (id, name) VALUES (?, ?)",
            ("cat1", "Test Category")
        )
        cursor.execute(
            "INSERT INTO pictograms "
            "(id, category_id, label, voice_command, icon_path) "
            "VALUES (?, ?, ?, ?, ?)",
            ("pic1", "cat1", "Test Label", "Test Voice", "path/to/icon.png")
        )
        conn.commit()


    return mgr

@pytest.fixture
def service(db_manager: DatabaseManager) -> PictogramService:
    return PictogramService(db_manager) # Changed db_manager=db_manager to db_manager

def test_default_category(service: PictogramService) -> None:
    cat = service.default_category
    assert cat.id == "cat1"
    assert cat.name == "Test Category"

def test_categories_generator(service: PictogramService) -> None:
    cats = list(service.categories)
    assert len(cats) == 1
    assert cats[0].id == "cat1"

def test_get_pictogram_by_id(service: PictogramService) -> None:
    pic = service["pic1"]
    assert pic is not None
    assert pic.label == "Test Label"

    assert service["nonexistent"] is None


def test_service_mapping_and_iter(service: PictogramService) -> None:
    cats = list(service)
    assert len(cats) == 1
    assert cats[0].name == "Test Category"

def test_deprecated_methods(service: PictogramService) -> None:
    # Ensure backward compatibility
    cat = service.get_main_category()
    assert cat.id == "cat1"
    pic = service.get_pictogram_by_id("pic1")
    assert pic is not None
    assert pic.label == "Test Label"


