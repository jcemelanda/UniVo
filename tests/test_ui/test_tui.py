from typing import Any
from unittest.mock import PropertyMock, patch

import pytest

from univo.core.domain import Category, Pictogram
from univo.ui.tui.app import UniVoTUIApp


@pytest.fixture
def mock_service() -> Any:
    with patch("univo.ui.tui.app.PictogramService") as mock_service_class:
        instance = mock_service_class.return_value
        
        # Mock categories property
        mock_category = Category(
            id="cat1", 
            name="Test Category", 
            pictograms=[
                Pictogram(
                    id="p1", 
                    label="Pic 1", 
                    voice_command="p1", 
                    image_path="p1.png"
                )
            ]
        )
        # Use type() to set property-like behavior on the mock instance
        type(instance).categories = PropertyMock(return_value=[mock_category])
        instance.get_pictogram_by_id.side_effect = lambda pid: (
            Pictogram(id=pid, label=pid, voice_command=pid) 
            if pid in ["yes", "no", "p1"] else None
        )
        instance.get_category_by_id.return_value = mock_category
        
        yield instance

@pytest.mark.asyncio
async def test_tui_layout(mock_service: Any) -> None:
    app = UniVoTUIApp()

    async with app.run_test():
        # Home view shows categories
        assert app.query_one("#btn-yes")
        assert app.query_one("#btn-no")
        assert app.query_one("#cat-cat1")

@pytest.mark.asyncio
async def test_tui_navigation(mock_service: Any) -> None:
    app = UniVoTUIApp()

    async with app.run_test() as pilot:
        # Click category to enter it
        await pilot.click("#cat-cat1")
        assert app.query_one("#btn-p1")

        # Click Home to go back
        await pilot.click("#btn-home")
        assert app.query_one("#cat-cat1")

@pytest.mark.asyncio
async def test_tui_interaction(mock_service: Any) -> None:
    app = UniVoTUIApp()

    async with app.run_test() as pilot:
        await pilot.click("#cat-cat1")
        await pilot.click("#btn-p1")
        assert pilot is not None
