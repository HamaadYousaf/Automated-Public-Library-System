from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DATABASE_NAME")]
books_collection = db["books"]

class Book(BaseModel):
    title: str
    author: str
    published_year: int
    genre: str
    available_copies: Optional[int] = 1