import pytest

from univo.core.domain import Category, Pictogram


def test_pictogram_and_category() -> None:
    """Verify Category behaves like a sequence."""
    p1 = Pictogram(id="p1", label="Pic 1")
    p2 = Pictogram(id="p2", label="Pic 2")
    
    cat = Category(id="c1", name="Test Cat", pictograms=[p1, p2])
    
    # Test __len__
    expected_len = 2
    assert len(cat) == expected_len
    
    # Test __getitem__
    assert cat[0] == p1
    assert cat[1] == p2
    
    # Test __iter__
    items = list(cat)
    assert len(items) == expected_len
    assert items[0] == p1
    
    # Test __str__
    assert "Test Cat" in str(cat)
    assert "2 items" in str(cat)
    
    # Test __repr__
    assert "Category(id='c1'" in repr(cat)
    assert "Pictogram(id='p1'" in repr(p1)

    # Test __contains__
    assert "p1" in cat
    assert p1 in cat
    assert "p3" not in cat
    
    # Test __add__
    p3 = Pictogram(id="p3", label="Pic 3")
    cat2 = Category(id="c2", name="Second Cat", pictograms=[p3])
    combined = cat + cat2
    combined_len = 3
    assert len(combined) == combined_len
    assert combined.id == "c1+c2"
    assert "Test Cat & Second Cat" == combined.name
    
    # Test __getattr__ (dynamic access)
    assert cat.p1 == p1
    assert cat.p2 == p2
    with pytest.raises(AttributeError):
        _ = cat.nonexistent
