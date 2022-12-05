import sys
sys.path.append("..")

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi_pagination import paginate, Page

import database_crud as db_crud
from schemas import User, WatchlistInput, Watchlist, WatchlistMovie

router = APIRouter(prefix="/v1")


@router.post("/watchlist/movies", response_model=Watchlist, summary="Add a movie in user's watchlist", tags=["Watchlists"])
def add_movie_to_watchlist(watchlistInput: WatchlistInput, user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Adds a movie in the user's watchlist
    """
    try:
        return db_crud.add_movie_to_watchlist(db, movie_id=watchlistInput.movie_id, user_email=user.email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/watchlist/movies", response_model=Page[WatchlistMovie], summary="Get movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_movies(user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Returns movies from user's watchlist.
    """
    try:
        return paginate(db_crud.get_watchlist_movies(db, user.email))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/watchlist/watched/movies", response_model=Page[WatchlistMovie], summary="Get watched movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_watched_movies(user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Returns watched movies from user's watchlist.
    """
    try:
        return paginate(db_crud.get_watchlist_watched_movies(db, user.email))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/watchlist/upcoming/movies", response_model=Page[WatchlistMovie], summary="Get upcoming movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_upcoming_movies(user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Returns upcoming movies from user's watchlist.
    """
    try:
        return paginate(db_crud.get_watchlist_upcoming_movies(db, user.email))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.get("/watchlist/movies/{movie_id}", response_model=WatchlistMovie, summary="Get a movie from user's watchlist", tags=["Watchlists"])
def get_watchlist_movie(movie_id: int, user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Returns a movie from user's watchlist.
    """
    try:
        return db_crud.get_watchlist_movie(db, movie_id, user.email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.delete("/watchlist/movies/{movie_id}", summary="Remove a movie from user's watchlist", tags=["Watchlists"])
def remove_watchlist_movie(movie_id: int, user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Returns movies from user's watchlist.
    """
    try:
        db_crud.remove_movie_from_watchlist(
            db, movie_id=movie_id, user_email=user.email)
        return {"result": f"Movie with ID {movie_id} has been removed from your watchlist."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@router.put("/watchlist/movies/{movie_id}/watch", response_model=WatchlistMovie, summary="Mark a movie from user's watchlist as watched", tags=["Watchlists"])
def watch_movie(movie_id: int, user: User = Depends(db_crud.get_current_user), db: Session = Depends(db_crud.get_db)):
    """
    Marks a movie from user's watchlist
    as watched
    """
    try:
        return db_crud.watch_movie(db, movie_id, user.email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except db_crud.TooSoonException as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")
