import sys
sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import database_crud as db_crud
from schemas import Movie, MovieDetails
from typing import List


router = APIRouter(prefix="/v1")


@router.get("/movies", response_model=List[MovieDetails], summary="Get all movies", tags=["Movies"])
def get_all_movies(db: Session = Depends(db_crud.get_db)):
    """
    Returns all movies.
    """
    try:
        return db_crud.get_movies(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.post("/movies", response_model=MovieDetails, summary="Add a movie", tags=["Movies"])
def post_movie(movie: Movie, db: Session = Depends(db_crud.get_db)):
    """
    Posts a movie.
    """
    try:
        return db_crud.add_movie(db, movie)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/movies/{movie_id}", response_model=MovieDetails, summary="Get a movie by ID", tags=["Movies"])
def get_movie_by_id(movie_id: int, db: Session = Depends(db_crud.get_db)):
    """
    Returns a movie by ID.
    """
    try:
        return db_crud.get_movie(db, movie_id=movie_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.delete("/movies/{movie_id}", summary="Delete a movie by ID", tags=["Movies"])
def delete_movie_by_id(movie_id: int, db: Session = Depends(db_crud.get_db)):
    """
    Deletes a movie by ID.
    """
    try:
        db_crud.delete_movie(db, movie_id=movie_id)
        return {"result": f"Movie with ID {movie_id} has been deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/movies/search/", response_model=List[MovieDetails], summary="Search for movies based on title keyword", tags=["Movies"])
def movies_search(keyword: str, db: Session = Depends(db_crud.get_db)):
    """
    Returns all movies 
    that include the given keyword
    in their title
    """
    try:
        return db_crud.search_movies(db, keyword=keyword)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/movies/upcoming/", response_model=List[MovieDetails], summary="Get upcoming movies", tags=["Movies"])
def get_upcoming_movies(db: Session = Depends(db_crud.get_db)):
    """
    Returns upcoming movies.
    """
    try:
        return db_crud.get_upcoming_movies(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")
