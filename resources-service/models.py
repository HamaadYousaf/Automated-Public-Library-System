"""
Library Resource Model with Custom Field Ordering
Fields appear in this exact order in Swagger UI and API docs:
1. title
2. author
3. published_year
4. genre
5. media_type
6. available_copies
7. image
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, validator
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]
books_collection = db["books"]

class MediaType(str, Enum):
    """Supported media formats"""
    BOOK = "book"
    EBOOK = "e-book"
    AUDIOBOOK = "audiobook"

class Book(BaseModel):
    """
    Complete model with custom field ordering and Shakespeare examples
    
    """
    
    # Field ordering matches your exact requirements
    title: str = Field(
        ...,
        example="Hamlet",
        description="[REQUIRED] Title of the work",
        position=0
    )
    
    author: str = Field(
        ...,
        example="William Shakespeare",
        description="[REQUIRED] Author's full name",
        position=1
    )
    
    published_year: int = Field(
        ...,
        example=1603,
        ge=1400,
        le=2025,
        description="[REQUIRED] Publication year (1400-2025)",
        position=2
    )
    
    genre: str = Field(
        ...,
        example="Tragedy",
        description="[REQUIRED] Literary genre/category",
        position=3
    )
    
    media_type: MediaType = Field(
        ...,
        example="book",
        description=f"[REQUIRED] Format type: {[e.value for e in MediaType]}",
        position=4
    )
    
    available_copies: int = Field(
        default=1,
        example=1,
        description="[OPTIONAL] Available copies (default: 1)",
        position=5
    )
    
    image: Optional[HttpUrl] = Field(
        default=None,
        example="https://example.com/book-cover.jpg",
        description="[OPTIONAL] Cover image URL",
        position=6
    )

    class Config:
        # Ensures fields appear in this exact order everywhere
        fields = {
            'title': {'position': 0},
            'author': {'position': 1},
            'published_year': {'position': 2},
            'genre': {'position': 3},
            'media_type': {'position': 4},
            'available_copies': {'position': 5},
            'image': {'position': 6}
        }
        
        # Example shown in Swagger UI
        schema_extra = {
            "example": {
                "title": "Hamlet",
                "author": "William Shakespeare",
                "published_year": 1603,
                "genre": "Tragedy",
                "media_type": "book",
                "[OPTIONAL] available_copies": 1 ,
                "[OPTIONAL] image": "https://example.com/book-cover.jpg"
            }
        }

    @validator('available_copies', always=True)
    def set_digital_defaults(cls, v, values):
        """Auto-sets unlimited copies for digital items"""
        if 'media_type' in values and values['media_type'] in [MediaType.EBOOK, MediaType.AUDIOBOOK]:
            return 9999
        return v