import pytest
from pydantic import ValidationError

from bookshelf.models import BookCreate, ReviewCreate


def test_book_create_valid():
    book = BookCreate(
        title="The Pragmatic Programmer",
        author="David Thomas",
        isbn="9780135957059",
        year=1999,
    )
    assert book.title == "The Pragmatic Programmer"
    assert book.isbn == "9780135957059"
    assert book.year == 1999


def test_book_create_strips_isbn_hyphens():
    book = BookCreate(
        title="Clean Code",
        author="Robert Martin",
        isbn="978-0-13-235088-4",  # hyphenated form
        year=2008,
    )
    assert book.isbn == "9780132350884"  # hyphens removed by validator


def test_book_create_invalid_isbn_raises():
    with pytest.raises(ValidationError) as exc_info:
        BookCreate(title="X", author="Y", isbn="123", year=2020)
    assert "ISBN" in str(exc_info.value)