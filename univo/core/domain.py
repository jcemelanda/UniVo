from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Pictogram:
    """Represents a single communication unit with an image and voice command.
    
    Attributes:
        id: Unique identifier for the pictogram.
        label: Human-readable text displayed with the pictogram.
        image_path: Path to the image file relative to resources.
        voice_command: The text to be spoken by TTS when selected.
    """
    id: str
    label: str
    image_path: str | None = None
    voice_command: str | None = None

    def __str__(self) -> str:
        """User-friendly representation (e.g., 'Yes (yes)')."""
        return f"{self.label} ({self.id})"

    def __repr__(self) -> str:
        """Formal developer representation."""
        return f"Pictogram(id={self.id!r}, label={self.label!r})"


@dataclass(slots=True)
class Category:
    """A collection of pictograms grouped by theme.
    
    Implements the Sequence protocol (__len__, __getitem__, __iter__)
    allowing it to be used like an immutable list of pictograms.
    Supports dynamic attribute access for getting pictograms by ID.
    """
    id: str
    name: str
    pictograms: list[Pictogram]

    def __len__(self) -> int:
        """Returns the number of pictograms in the category."""
        return len(self.pictograms)

    def __getitem__(self, position: int | slice) -> Any:
        """Supports indexing and slicing (Sequence protocol)."""
        return self.pictograms[position]

    def __iter__(self) -> Iterator[Pictogram]:
        """Iterates over the pictograms (Sequence protocol)."""
        return iter(self.pictograms)
    
    def __str__(self) -> str:
        """User-friendly summary of the category."""
        return f"Category: {self.name} ({len(self)} items)"

    def __repr__(self) -> str:
        """Formal developer representation."""
        return f"Category(id={self.id!r}, name={self.name!r}, items={len(self)})"

    def __contains__(self, item: object) -> bool:
        """Checks if a pictogram or pictogram ID belongs to this category."""
        if isinstance(item, str):
            return any(p.id == item for p in self.pictograms)
        if isinstance(item, Pictogram):
            return item in self.pictograms
        return False

    def __add__(self, other: Category) -> Category:
        """Merges two categories into a new one (Fluent Python style)."""
        if not isinstance(other, Category):
            return NotImplemented
        new_id = f"{self.id}+{other.id}"
        new_name = f"{self.name} & {other.name}"
        return Category(
            id=new_id, 
            name=new_name, 
            pictograms=self.pictograms + other.pictograms
        )

    def __getattr__(self, name: str) -> Pictogram:
        """Allows dynamic access to pictograms using category.pictogram_id."""
        for p in self.pictograms:
            if p.id == name:
                return p
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )



