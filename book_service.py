import pymongo
from bson import ObjectId
from pymongo.collection import Collection

from book import Book


def get_bs_collection () -> Collection:
    mcli = pymongo.MongoClient("mongodb://localhost:27017")
    db = mcli["library"]

    return db["book-service"]

def insert_book (book: Book) -> ObjectId:
    mdb = get_bs_collection()

    if query_book_with_title(book.title) is not None:
        return None

    result = mdb.insert_one(book.to_insert())

    return result.inserted_id

def query_book_with_title (book_title: str) -> Book:
    mdb = get_bs_collection()

    result = mdb.find_one({ "title": book_title })
    if result is None:
        return None

    return Book(**result)

def increase_book_amount (book_title: str, amount: int) -> bool:
    mdb = get_bs_collection()

    result = mdb.update_one(
        { "title": book_title },
        { "$inc": { "amount": amount } }
    )

    return result.acknowledged and result.modified_count == 1

def decrease_book_amount (book_title: str, amount: int) -> bool:
    mdb = get_bs_collection()

    result = mdb.update_one(
        { "title": book_title, "amount": { "$gte": amount } },
        { "$inc": { "amount": -amount } }
    )

    return result.acknowledged and result.modified_count == 1

