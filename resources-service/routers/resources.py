"""
API endpoints for managing library resources
"""
from fastapi import APIRouter, HTTPException, status
from models import Book, books_collection, MediaType

router = APIRouter(
    prefix="/api/books",
    tags=["Books"],
    responses={404: {"description": "Resource not found"}}
)

@router.post("/", 
            status_code=status.HTTP_201_CREATED,
            summary="Add new resource or update existing copies",
            response_description="Details of added/updated resource")
async def add_book(book: Book):
    """
    Handles resource additions:
    - Creates new entry if resource doesn't exist
    - Updates copies/licenses if resource exists
    - Case-insensitive title/author matching
    - Automatic media type handling
    """
    try:
        # Check for existing resource using case-insensitive match
        existing_book = books_collection.find_one({
            "title": {"$regex": f"^{book.title}$", "$options": "i"},
            "author": {"$regex": f"^{book.author}$", "$options": "i"},
            "media_type": book.media_type
        })

        if existing_book:
            # Update existing resource copies/licenses
            updated = books_collection.update_one(
                {"_id": existing_book["_id"]},
                {"$inc": {"available_copies": book.available_copies}}
            )
            # Return updated resource information
            updated_book = books_collection.find_one({"_id": existing_book["_id"]})
            return {
                "id": str(updated_book["_id"]),
                "message": "Existing resource updated",
                "new_total": updated_book["available_copies"]
            }
        else:
            # Insert new resource into database
            result = books_collection.insert_one(book.dict())
            return {
                "id": str(result.inserted_id),
                "message": "New resource added",
                "current_copies": book.available_copies
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("/",
           summary="Search resources with filters",
           response_description="List of matching resources")
async def search_books(
    title: str = "",
    author: str = "",
    genre: str = "",
    media_type: MediaType = None
):
    """
    Search resources by:
    - Title (case-insensitive partial match)
    - Author (case-insensitive partial match)
    - Genre (exact match)
    - Media type (exact match)
    """
    try:
        query = {}
        # Build search query dynamically
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        if genre:
            query["genre"] = genre
        if media_type:
            query["media_type"] = media_type.value

        # Convert MongoDB documents to API-friendly format
        books = []
        for doc in books_collection.find(query):
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            books.append(doc)
        
        return books
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}"
        )