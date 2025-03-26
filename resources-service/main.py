"""
Main application setup with CORS and error handling
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.resources import router as books_router  # Ensure this import matches your file structure
from dotenv import load_dotenv

# Load environment variables (for MongoDB credentials)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Automated Library System",
    description="API for managing physical/digital library resources",
    version="2.3",
    docs_url="/docs"  # Access Swagger UI at http://localhost:8000/docs
)

# ================== CORS Configuration ==================
# Required for frontend communication (e.g., React/Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with your frontend URL in production)
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ================== Include Routes ==================
app.include_router(books_router)  # Connects your resources.py endpoints

# ================== Health Check ==================
@app.get("/Status", tags=["System"])
def ServerStatus():
    """Verify server status"""
    return {"status": "active"}