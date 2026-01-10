
import pytest

from univo.core.i18n import I18nManager, _, i18n


@pytest.fixture
def i18n_manager() -> I18nManager:
    """Returns a fresh I18nManager instance."""
    return i18n

def test_i18n_singleton() -> None:
    i1 = I18nManager()
    i2 = I18nManager()
    assert i1 is i2

def test_available_languages(i18n_manager: I18nManager) -> None:
    langs = i18n_manager.available_languages
    assert "en" in langs
    assert "pt" in langs

def test_default_language(i18n_manager: I18nManager) -> None:
    # App should default to English
    assert i18n_manager.current_language == "en"

def test_translation_switching(i18n_manager: I18nManager) -> None:
    # Switch to PT
    i18n_manager.load_language("pt")
    assert i18n_manager.current_language == "pt"
    assert i18n_manager.translate("Home") == "Início"
    
    # Switch back to EN
    i18n_manager.load_language("en")
    assert i18n_manager.current_language == "en"
    assert i18n_manager.translate("Home") == "Home"

def test_translate_fallback(i18n_manager: I18nManager) -> None:
    # Unknown key should return key itself
    assert i18n_manager.translate("UnknownKey") == "UnknownKey"

def test_underscore_alias() -> None:
    # Test the global alias
    assert _("UniVo") == "UniVo"
