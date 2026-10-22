import sqlite3
from collections.abc import Generator
from pathlib import Path

import pytest
from bookshelf import services
from bookshelf.database import _create_schema
from bookshelf.models import BookCreate


@pytest.fixture
def db_conn(tmp_path: Path) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(tmp_path / "test.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _create_schema(conn)
    yield conn
    conn.close()


@pytest.fixture
def books_in_db(db_conn: sqlite3.Connection) -> sqlite3.Connection:
    for book in [
        BookCreate(
            title="Clean Code", author="Robert Martin", isbn="9780132350884", year=2008
        ),
        BookCreate(
            title="The Pragmatic Programmer",
            author="David Thomas",
            isbn="9780135957059",
            year=1999,
        ),
        BookCreate(
            title="Design Patterns",
            author="Gang of Four",
            isbn="9780201633610",
            year=1994,
        ),
    ]:
        services.create_book(db_conn, book)
    return db_conn


def test_search_books_by_title(books_in_db: sqlite3.Connection) -> None:
    results = services.search_books(books_in_db, "Clean")
    assert len(results) == 1
    assert results[0].title == "Clean Code"


def test_search_books_by_author(books_in_db: sqlite3.Connection) -> None:
    results = services.search_books(books_in_db, "Martin")
    assert len(results) == 1
    assert results[0].author == "Robert Martin"


def test_search_books_partial_match(books_in_db: sqlite3.Connection) -> None:
    results = services.search_books(books_in_db, "Prag")
    assert len(results) == 1
    assert results[0].title == "The Pragmatic Programmer"


def test_search_books_no_results(books_in_db: sqlite3.Connection) -> None:
    results = services.search_books(books_in_db, "Kubernetes")
    assert results == []
