"""
Main FastAPI application setup
"""
from fastapi import FastAPI
from routers.resources import router as books_router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Library Books Service",
    description="API for managing library book inventory and search",
    version="1.2.0"
)

# Include book management routes
app.include_router(books_router)

@app.get("/status", summary="Check system status")
def system_status():
    """Returns current API status"""
    return {"status": "operational"}