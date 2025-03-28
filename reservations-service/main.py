from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import re
from bson import ObjectId

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
BOOKS_COLLECTION_NAME = "books"
RESERVATIONS_COLLECTION_NAME = "reservations"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
books_collection = db[BOOKS_COLLECTION_NAME]
reservations_collection = db[RESERVATIONS_COLLECTION_NAME]

# Helper function to clean input text
def clean_text(text: str):
    return re.sub(r"\s+", " ", text).strip()

# Helper function to find books by title
def find_book(book_name: str):
    book_name = clean_text(book_name)
    return books_collection.find_one({
        "title": {"$regex": f"^{re.escape(book_name)}$", "$options": "i"}
    })

# Check book availability
@app.get("/available/{book_name}")
def check_availability(book_name: str):
    book = find_book(book_name)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in the collection.")
    return {"available": book["available_copies"] > 0}

# Reserve a book (ONLY if all copies are out of stock)
@app.post("/reserve/")
def reserve_book(user_id: str, book_name: str):
    book_name = clean_text(book_name)
    book = find_book(book_name)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in the collection.")
    
    if book["available_copies"] > 0:
        raise HTTPException(status_code=400, detail="Book is available. No need to reserve.")

    existing_reservation = reservations_collection.find_one(
        {"book_name": book_name, "user_id": user_id, "status": "reserved"}
    )
    if existing_reservation:
        raise HTTPException(status_code=400, detail="You have already reserved this book.")

    reservation = {
        "user_id": user_id,
        "book_name": book_name,
        "status": "reserved",
        "due_date": datetime.utcnow() + timedelta(days=7),  # 1 week
        "reserved_at": datetime.utcnow()
    }
    reservations_collection.insert_one(reservation)

    return {"message": "Book reserved successfully.", "due_date": reservation["due_date"]}

# Borrow a book (2-week max borrow time)
@app.post("/borrow/")
def borrow_book(user_id: str, book_name: str):
    book_name = clean_text(book_name)

    reservation = reservations_collection.find_one(
        {"book_name": book_name, "user_id": user_id, "status": "reserved"}
    )

    if reservation:
        update_result = reservations_collection.update_one(
            {"_id": ObjectId(reservation["_id"])},
            {"$set": {"status": "borrowed", "due_date": datetime.utcnow() + timedelta(days=14)}}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update reservation status.")

        return {"message": "Reserved book borrowed successfully.", "due_date": datetime.utcnow() + timedelta(days=14)}

    book = find_book(book_name)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found in the collection.")
    if book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="Book is out of stock.")

    books_collection.update_one({"_id": book["_id"]}, {"$inc": {"available_copies": -1}})

    reservation = {
        "user_id": user_id,
        "book_name": book_name,
        "status": "borrowed",
        "due_date": datetime.utcnow() + timedelta(days=14),
        "borrowed_at": datetime.utcnow()
    }
    reservations_collection.insert_one(reservation)

    return {"message": "Book borrowed successfully.", "due_date": reservation["due_date"]}

# Renew a book (adds 1 week to current due date)
@app.post("/renew/")
def renew_book(user_id: str, book_name: str):
    book_name = clean_text(book_name)

    reservation = reservations_collection.find_one(
        {"book_name": book_name, "user_id": user_id, "status": "borrowed"}
    )
    if not reservation:
        raise HTTPException(status_code=400, detail="No active loan found for this book.")

    new_due_date = reservation["due_date"] + timedelta(days=7)
    
    reservations_collection.update_one(
        {"_id": ObjectId(reservation["_id"])},
        {"$set": {"due_date": new_due_date}}
    )

    return {"message": "Book renewed successfully.", "new_due_date": new_due_date}

# Return a book (increases available copies)
@app.post("/return/")
def return_book(user_id: str, book_name: str):
    book_name = clean_text(book_name)

    reservation = reservations_collection.find_one(
        {"book_name": book_name, "user_id": user_id, "status": "borrowed"}
    )
    if not reservation:
        raise HTTPException(status_code=400, detail="No active loan found for this book.")

    # Update reservation status to "returned"
    update_result = reservations_collection.update_one(
        {"_id": ObjectId(reservation["_id"])},
        {"$set": {"status": "returned"}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update reservation status.")

    # Increase book count in the library
    book = find_book(book_name)
    if book:
        books_collection.update_one({"_id": book["_id"]}, {"$inc": {"available_copies": 1}})

    return {"message": "Book returned successfully."}
