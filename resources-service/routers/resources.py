"""
API endpoints for resource management with proper optional field handling
"""

from fastapi import APIRouter, HTTPException, status, Query
from models import Book, books_collection, MediaType
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

router = APIRouter(
    prefix="/api/books",
    tags=["Books"],
    responses={404: {"description": "Resource not found"}}
)

@router.post("/", 
            status_code=status.HTTP_201_CREATED,
            summary="Add new resource",
            response_description="Details of added/updated resource")
async def add_book(book: Book):
    """
    Handles resource creation/updates with smart defaults:
    - Sets available_copies=1 for physical books if not provided
    - Sets available_copies=9999 for digital items if not provided
    - Properly handles optional image field
    - Updates existing physical books by adding copies
    """
    try:
        # Convert Pydantic model to dictionary and process fields
        book_data = book.dict()
        
        # --- Handle Image Field ---
        # Convert HttpUrl to string if image exists, otherwise remove None values
        if book_data.get("image"):
            book_data["image"] = str(book_data["image"])
        elif "image" in book_data:
            del book_data["image"]  # Remove None values from the data
            
        # --- Handle Available Copies ---
        # Set default copies if not provided in request
        if "available_copies" not in book_data:
            book_data["available_copies"] = (
                1 if book.media_type == MediaType.BOOK 
                else 9999  # Unlimited for digital items
            )
        
        # --- Check for Existing Resource ---
        # Case-insensitive search for duplicates
        existing = books_collection.find_one({
            "title": {"$regex": f"^{book.title}$", "$options": "i"},
            "author": {"$regex": f"^{book.author}$", "$options": "i"},
            "media_type": book.media_type
        })

        # --- Existing Item Handling ---
        if existing:
            # Digital items should not update copies
            if existing["media_type"] in [MediaType.EBOOK.value, MediaType.AUDIOBOOK.value]:
                return {
                    "id": str(existing["_id"]),
                    "message": "Digital resource already exists",
                    "available_copies": existing["available_copies"],
                    "image": existing.get("image")
                }
            
            # For physical books: increment copies
            increment_amount = book_data["available_copies"]
            books_collection.update_one(
                {"_id": existing["_id"]},
                {"$inc": {"available_copies": increment_amount}}
            )
            updated = books_collection.find_one({"_id": existing["_id"]})
            return {
                "id": str(updated["_id"]),
                "message": f"Added {increment_amount} copies to existing resource",
                "new_total": updated["available_copies"],
                "image": updated.get("image")
            }
        
        # --- New Item Creation ---
        else:
            result = books_collection.insert_one(book_data)
            return {
                "id": str(result.inserted_id),
                "message": "New resource added successfully",
                "current_copies": book_data["available_copies"],
                "image": book_data.get("image")
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed: {str(e)}"
        )

@router.get("/",
           summary="Search resources",
           response_description="List of matching resources")
async def search_books(
    title: str = Query(None, description="Partial title match"),
    author: str = Query(None, description="Partial author match"),
    genre: str = Query(None, description="Exact genre match"),
    media_type: MediaType = Query(None, description="Filter by format"),
    sort_by: str = Query("title", enum=["title", "author", "published_year"]),
    sort_order: str = Query("asc", enum=["asc", "desc"])
):
    """Search endpoint with filters and sorting"""
    try:
        query = {}
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        if genre:
            query["genre"] = genre
        if media_type:
            query["media_type"] = media_type.value

        sort_dir = ASCENDING if sort_order == "asc" else DESCENDING
        resources = []
        
        for doc in books_collection.find(query).sort(sort_by, sort_dir):
            doc["_id"] = str(doc["_id"])
            resources.append(doc)
            
        return resources

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )