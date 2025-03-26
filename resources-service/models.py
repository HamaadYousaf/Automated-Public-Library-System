"""
Database models and connection setup for library resources
"""
from enum import Enum
from pydantic import BaseModel, Field
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Establish MongoDB connection using credentials from .env
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]
books_collection = db["books"]

class MediaType(str, Enum):
    """
    Enumeration of supported media types
    - book: Physical book
    - e-book: Digital ebook format
    - audiobook: Audio recording format
    """
    BOOK = "book"
    EBOOK = "e-book"
    AUDIOBOOK = "audiobook"

class Book(BaseModel):
    """
    Data model representing a library resource
    - Validates input data types and values
    - Provides default values where applicable
    """
    title: str = Field(..., example="Hamlet", description="Title of the resource")
    author: str = Field(..., example="William Shakespeare", description="Author/creator")
    published_year: int = Field(..., example=1603, description="Year of publication")
    genre: str = Field(..., example="Tragedy", description="Genre/category")
    media_type: MediaType = Field(
        default=MediaType.BOOK,
        description="Format of the resource"
    )
    available_copies: int = Field(
        default=1,
        ge=0,
        example=2,
        description="Available units/copies (physical) or licenses (digital)"
    )