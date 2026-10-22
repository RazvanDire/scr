import sqlite3

from bookshelf.models import BookCreate, BookResponse


def search_books(conn: sqlite3.Connection, query: str) -> list[BookResponse]:
    rows = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{query}%", f"%{query}%"),
    ).fetchall()
    return [BookResponse(**dict(row)) for row in rows]


def create_book(conn: sqlite3.Connection, book: BookCreate) -> BookResponse:
    cursor = conn.execute(
        "INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)",
        (book.title, book.author, book.isbn, book.year),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM books WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return BookResponse(**dict(row))


def calculate_average_rating(ratings: list[int]) -> float | None:
    if not ratings:
        return None
    return sum(ratings) / len(ratings)
