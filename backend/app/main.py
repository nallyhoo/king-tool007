
from fastapi import FastAPI
from app.search import create_index, search_videos

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_index()

@app.get("/search")
def search(query: str):
    return search_videos(query)
