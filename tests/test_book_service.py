import pytest
import mongomock
from bson import ObjectId

import book_service as bs
from book import Book



class TestBookService:
    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_insert_empty_book (self) -> None:
        book = Book("empty-book")

        result = bs.insert_book(book)

        assert book._id == result

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_insert_book_with_all_attributes (self) -> None:
        book_id = ObjectId()
        book = Book("full-book", "teste", 15, 1, book_id)

        assert book_id == bs.insert_book(book)

        assert book == bs.query_book_with_title("full-book")

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_query_book_with_empty_collection (self) -> None:
        assert bs.query_book_with_title("empty-book") is None

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_query_book_after_insert (self) -> None:
        book = Book("empty-book")

        book._id = bs.insert_book(book)
        query = bs.query_book_with_title("empty-book")

        assert book == query

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_insert_book_title_twice (self) -> None:
        book = Book("empty-book")

        bs.insert_book(book)

        assert bs.insert_book(book) is None

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_increase_book_amount (self) -> None:
        book = Book("empty-book", amount = 0)

        bs.insert_book(book)

        assert bs.increase_book_amount("empty-book", 2)

        result = bs.query_book_with_title("empty-book")

        assert result.amount == 2

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_failed_decrease_book_amount (self) -> None:
        book = Book("empty-book", amount = 0)

        bs.insert_book(book)

        assert not bs.decrease_book_amount("empty-book", 1)

    @mongomock.patch(servers="mongodb://localhost:27017")
    def test_sucessful_decrease_book_amount (self) -> None:
        book = Book("empty-book", amount=1)

        bs.insert_book(book)
        assert bs.decrease_book_amount("empty-book", 1)

        result = bs.query_book_with_title("empty-book")

        assert result.amount == 0

