from fastapi import APIRouter, HTTPException, status
from models import Book, books_collection
from datetime import datetime

router = APIRouter(prefix="/api/books", tags=["Books"])

@router.post("/", status_code=status.HTTP_200_OK)
async def add_book(book: Book):
    # Case-insensitive exact match check
    existing_book = books_collection.find_one({
        "title": {"$regex": f"^{book.title}$", "$options": "i"},
        "author": {"$regex": f"^{book.author}$", "$options": "i"}
    })

    if existing_book:
        # Update existing book's copies
        updated = books_collection.update_one(
            {"_id": existing_book["_id"]},
            {"$inc": {"available_copies": book.available_copies}}
        )
        return {
            "id": str(existing_book["_id"]),
            "warning": "Existing book updated",
            "new_total_copies": existing_book["available_copies"] + book.available_copies
        }
    else:
        # Add new book
        new_book = book.dict()
        new_book["added_at"] = datetime.utcnow()
        result = books_collection.insert_one(new_book)
        return {
            "id": str(result.inserted_id),
            "message": "New book added",
            "current_copies": book.available_copies
        }