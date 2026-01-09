import sys
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest

from univo.core.domain import Category, Pictogram


@pytest.fixture
def mock_toga_env() -> Any:
    """Completely mock toga and its dependencies."""
    mock_toga = MagicMock()
    
    # Define a dummy App class that our app can inherit from
    class DummyApp:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.formal_name = args[0] if args else "UniVo"
            self.main_window = MagicMock()
            
        def main_loop(self) -> None:
            pass

    mock_toga.App = DummyApp
    mock_toga.MainWindow = MagicMock()
    mock_toga.Box = MagicMock()
    mock_toga.Label = MagicMock()
    mock_toga.Button = MagicMock()
    mock_toga.ScrollContainer = MagicMock()
    mock_toga.Icon = MagicMock()
    mock_toga.InfoDialog = MagicMock()

    
    toga_patch = {
        "toga": mock_toga, 
        "toga.style": MagicMock(), 
        "toga.style.pack": MagicMock()
    }
    with patch.dict(sys.modules, toga_patch):
        # Import (or re-import) the app module
        import univo.ui.toga.app  # noqa: PLC0415
        yield univo.ui.toga.app

@pytest.fixture
def mock_service() -> Any:
    with patch("univo.ui.toga.app.PictogramService") as mock_service_class:
        instance = mock_service_class.return_value
        mock_category = Category(
            id="cat1", 
            name="Test Category", 
            pictograms=[
                Pictogram(id="p1", label="Pic 1", voice_command="V1"),
                Pictogram(id="p2", label="Pic 2", voice_command="V2")
            ]
        )
        instance.default_category = mock_category
        instance.get_main_category.return_value = mock_category
        instance.get_pictogram_by_id.side_effect = (
            lambda pid: Pictogram(id="yes", label="Sim", voice_command="Sim") 
            if pid == "yes" else None
        )
            
        yield instance


def test_toga_startup(mock_toga_env: Any, mock_service: Any) -> None:
    app_module = mock_toga_env
    # Manually mock the service on the reloaded module
    mock_service_instance = MagicMock()
    app_module.PictogramService = mock_service_instance
    
    # Setup mock data for the instance (service.categories used in home render)
    mock_category = Category(
        id="cat1", 
        name="Test Category", 
        pictograms=[Pictogram(id="p1", label="Pic 1")]
    )
    mock_service_instance.return_value.categories = [mock_category]
    mock_service_instance.return_value.get_pictogram_by_id.return_value = None
    
    # We need to instantiate the class from the *reloaded* module
    app_class = app_module.UniVoTogaApp
    
    app = app_class("UniVo", "org.univo.app")
    app.startup()
    
    # Check if MainWindow was created
    import toga  # noqa: PLC0415
    assert cast(Any, toga.MainWindow).called
    
    # Verify Category Button creation (render_home)
    # The home view renders categories as buttons
    assert cast(Any, app_module.toga.Button).called
    
    # Check if "Test Category" label was passed to a Button (or nearby Label)
    calls = app_module.toga.Label.call_args_list
    found = any(c[0] and c[0][0] == "Test Category" for c in calls)
    assert found



