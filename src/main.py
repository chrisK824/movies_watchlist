import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database_crud, db_models
from database import SessionLocal, engine
from schemas import Movie, MovieDetails
from typing import List

db_models.Base.metadata.create_all(bind=engine)

def movies_watchlist_db():
    reviews_db = SessionLocal()
    try:
        yield reviews_db
    finally:
        reviews_db.close()

description = """
Movies watchlist API helps people
to easily list movies they want to watch by
adding new upcoming movies in their personal
list and track movies they have watched.

#### Users

You will be able to:

* Add a new movie.
* View upcoming movies.
* View all movies.
* Mark a movie as watched.
* View all watched movies.
"""

moviesWatchListAPI = FastAPI(
    title='Movies watchlist API',
    description=description,
    contact={
        "name": "Christos Karvouniaris",
        "email": "christos.karvouniaris247@gmail.com",
        "url" : "https://www.linkedin.com/in/chriskarvouniaris/"
    },
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs"
)

moviesWatchListAPI.add_middleware(CORSMiddleware, allow_origins=['*'])

@moviesWatchListAPI.get("/v1/movies", response_model=List[MovieDetails], summary ="Get all movies from watchlist", tags=["Movies"])
def get_movies(db: Session = Depends(movies_watchlist_db)):
    """
    Returns all movies from watchlist.
    """
    try:
        result = []
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/movies/watched", response_model=List[MovieDetails], summary ="Get watched movies from watchlist", tags=["Movies"])
def get_watched_movies(db: Session = Depends(movies_watchlist_db)):
    """
    Returns watched movies from watchlist.
    """
    try:
        result = []
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/movies/upcoming", response_model=List[MovieDetails], summary ="Get upcoming movies from watchlist", tags=["Movies"])
def get_upcoming_movies(db: Session = Depends(movies_watchlist_db)):
    """
    Returns upcoming movies from watchlist.
    """
    try:
        result = []
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/movies/{movie_id}", response_model=MovieDetails, summary ="Get a movie from watchlist by its ID", tags=["Movies"])
def get_movie(movie_id : int, db: Session = Depends(movies_watchlist_db)):
    """
    Returns a movie from watchlist
    """
    try:
        result = []
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.post("/v1/movies", response_model=MovieDetails, summary="Add a movie in the watchlist", tags=["Movies"])
def post_movie(movie : Movie, db: Session = Depends(movies_watchlist_db)):
    """
    Posts a movie in the watchlist.
    """
    try:
        result = {}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/movies/search", response_model=List[MovieDetails], summary ="Search for movies in watchlist based on title keyword", tags=["Movies"])
def movies_search(keyword : str, db: Session = Depends(movies_watchlist_db)):
    """
    Returns all movies in watchlist 
    that include the given keyword
    in their title
    """
    try:
        result = []
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.put("/v1/movies/{movie_id}", response_model=MovieDetails, summary="Mark a movie in the watchlist as watched", tags=["Movies"])
def watch_movie(movie_id : int, db: Session = Depends(movies_watchlist_db)):
    """
    Marks a movie in the watchlist
    as watched.
    """
    try:
        result = {}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

if __name__ == '__main__':
    uvicorn.run(moviesWatchListAPI, host="0.0.0.0", port=9999)
