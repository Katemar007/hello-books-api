from app.models.book import Book
import pytest

def test_from_dict_returns_book():
    # Arrange
    book_data = {
        "title": "Some new book",
        "description": "A really nice description"
    }
    # Act
    returned_book = Book.from_dict(book_data)
    # Assert
    assert returned_book.title == "Some new book"
    assert returned_book.description == "A really nice description"

def test_from_dict_no_title():
    # Arrange
    book_data = {"description": "A really nice description"}

    # Act
    with pytest.raises(KeyError, match = "title"):
        new_book = Book.from_dict(book_data)

def test_from_dict_no_description():
    # Arrange
    book_data = {"title": "Some new book"}

    # Act
    with pytest.raises(KeyError, match = "description"):
        new_book = Book.from_dict(book_data)

def test_from_dict_extra_keys():
    # Arrange
    book_data = {
        "extra": "Some extra",
        "key": "Some key",
        "title": "Some new book",
        "description": "A really nice description"
    }
    # Act
    returned_book = Book.from_dict(book_data)
    # Assert
    assert returned_book.title == "Some new book"
    assert returned_book.description == "A really nice description"

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Book(id = 1,
                    title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_id():
    # Arrange
    test_data = Book(title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_title():
    # Arrange
    test_data = Book(id=1, description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_description():
    # Arrange
    test_data = Book(id=1, title="Ocean Book")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] is None

