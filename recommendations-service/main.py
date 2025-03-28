from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
from random import sample

load_dotenv()
app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
users_collection = db["users"]
books_collection = db["books"]
reservations_collection = db["reservations"]


@app.post("/recommendations")
async def get_recommendations(email: str):
    """
    Retrieve a user's preferences, update them based on purchase history,
    and find books with genres matching the updated preferences,
    excluding books the user has already reserved.
    If the user has no preferences and no reservations, recommend 5 random books.
    """
    try:
        # Find the user by email
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        preferences = set(user.get("preferences", []))
        purchase_history = list(reservations_collection.find({"user_id": email}))

        # Collect the IDs of books the user has already reserved
        reserved_books = set()
        for reservation in purchase_history:
            book_id = reservation.get("book_name")
            if book_id:
                reserved_books.add(book_id)

        # Add genres from purchased books to preferences
        for reservation in purchase_history:
            book_id = reservation.get("book_name")
            if book_id:
                book = books_collection.find_one({"title": book_id})
                if book and "genre" in book:
                    preferences.add(book["genre"])

        # If the user has no preferences and no reservations, recommend 5 random books
        if not preferences and not reserved_books:
            random_books = list(books_collection.aggregate([{"$sample": {"size": 5}}]))
            for book in random_books:
                book["_id"] = str(book["_id"])
            return {
                "email": email,
                "updated_preferences": [],
                "recommended_books": random_books,
            }

        # Update the user's preferences in the database
        users_collection.update_one(
            {"email": email}, {"$set": {"preferences": list(preferences)}}
        )

        # Find books matching the updated preferences
        matching_books = list(
            books_collection.find(
                {
                    "genre": {"$in": list(preferences)},
                    "title": {"$nin": list(reserved_books)},
                }
            )
        )

        for book in matching_books:
            book["_id"] = str(book["_id"])

        # Select a random 5 books from the matching books
        limited_books = sample(matching_books, min(len(matching_books), 5))

        return {
            "email": email,
            "updated_preferences": list(preferences),
            "recommended_books": limited_books,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
