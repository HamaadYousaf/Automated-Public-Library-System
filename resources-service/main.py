from fastapi import FastAPI
from routers.resources import router as books_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Library Books Service",
    description="Manages book inventory for the library system"
)

app.include_router(books_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}