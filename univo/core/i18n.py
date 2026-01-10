import gettext
from pathlib import Path
from typing import Self, cast


class I18nManager:
    """Manages translations for the UniVo application using gettext."""
    
    _instance: Self | None = None
    
    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
            
        self.current_language = "en"
        self._locales_path = Path(__file__).parent.parent / "resources" / "lang"
        self._translation: gettext.NullTranslations | None = None
        self._initialized = True
        self.load_language(self.current_language)

    @property
    def available_languages(self) -> list[str]:
        """Returns a list of available language codes."""
        if not self._locales_path.exists():
            return ["en"]
        return [d.name for d in self._locales_path.iterdir() if d.is_dir()]

    def load_language(self, lang_code: str) -> None:
        """Loads a language using gettext."""
        try:
            self._translation = gettext.translation(
                'univo', 
                localedir=str(self._locales_path), 
                languages=[lang_code],
                fallback=True
            )
            if hasattr(self._translation, "install"):
                cast(Any, self._translation).install()
            self.current_language = lang_code
        except Exception as e:
            print(f"Error loading translation for {lang_code}: {e}")
            self._translation = gettext.NullTranslations()

    def translate(self, message: str) -> str:
        """Translates a message using the current gettext translation."""
        if self._translation:
            return self._translation.gettext(message)
        return message

# Final Any avoidance for mypy
from typing import Any  # noqa: E402

# Global instance for easy access
i18n = I18nManager()
_ = i18n.translate
