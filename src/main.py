import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import db_models
import database_crud as db_crud
from database import SessionLocal, engine
from schemas import UserSignUp, Movie, MovieDetails, WatchlistInput, Watchlist, WatchlistMovie
from typing import List, Optional

db_models.Base.metadata.create_all(bind=engine)


def get_db():
    movies_watchlists_db = SessionLocal()
    try:
        yield movies_watchlists_db
    finally:
        movies_watchlists_db.close()


description = """
Movies watchlist API helps people
to easily list movies they want to watch by
adding new upcoming movies in their personal
list and track movies they have watched.

#### Users

You will be able to:

* Add a new movie.
* View all movies.
* View upcoming movies.
* Add a movie in your watchlist.
* Mark a movie in your watchlist as watched.
* View watched movies.
* Remove a movie from your watchlist.
"""

moviesWatchListAPI = FastAPI(
    title='Movies watchlist API',
    description=description,
    contact={
        "name": "Christos Karvouniaris",
        "email": "christos.karvouniaris247@gmail.com",
        "url": "https://www.linkedin.com/in/chriskarvouniaris/"
    },
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs"
)

moviesWatchListAPI.add_middleware(CORSMiddleware, allow_origins=['*'])


@moviesWatchListAPI.post("/v1/signup", summary="Register a user", tags=["Users"])
def create_user(user: UserSignUp, db: Session = Depends(get_db)):
    """
    Registers a user.
    """
    try:
        db_crud.add_user(db, user)
        # TODO : actually send a verification email
        return {
            "resut": "You have successfully signed up. A verification email has been sent to your email address with a link to activate your acount."
        }
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.get("/v1/movies", response_model=List[MovieDetails], summary="Get all movies", tags=["Movies"])
def get_all_movies(db: Session = Depends(get_db)):
    """
    Returns all movies.
    """
    try:
        return db_crud.get_movies(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.post("/v1/movies", response_model=MovieDetails, summary="Add a movie", tags=["Movies"])
def post_movie(movie: Movie, db: Session = Depends(get_db)):
    """
    Posts a movie.
    """
    try:
        return db_crud.add_movie(db, movie)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.get("/v1/movies/{movie_id}", response_model=MovieDetails, summary="Get a movie by ID", tags=["Movies"])
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
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


@moviesWatchListAPI.delete("/v1/movies/{movie_id}", summary="Delete a movie by ID", tags=["Movies"])
def delete_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
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


@moviesWatchListAPI.get("/v1/movies/search/", response_model=List[MovieDetails], summary="Search for movies based on title keyword", tags=["Movies"])
def movies_search(keyword: str, db: Session = Depends(get_db)):
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


@moviesWatchListAPI.get("/v1/movies/upcoming/", response_model=List[MovieDetails], summary="Get upcoming movies", tags=["Movies"])
def get_upcoming_movies(db: Session = Depends(get_db)):
    """
    Returns upcoming movies.
    """
    try:
        return db_crud.get_upcoming_movies(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.post("/v1/watchlist/movies", response_model=Watchlist, summary="Add a movie in user's watchlist", tags=["Watchlists"])
def add_movie_to_watchlist(watchlistInput: WatchlistInput, db: Session = Depends(get_db)):
    """
    Adds a movie in the user's watchlist
    """
    try:
        return db_crud.add_movie_to_watchlist(db, movie_id=watchlistInput.movie_id, user_email=watchlistInput.user_email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.get("/v1/watchlist/movies", response_model=List[WatchlistMovie], summary="Get movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_movies(user_email: str, watched: Optional[bool] = False, db: Session = Depends(get_db)):
    """
    Returns movies from user's watchlist.
    """
    try:
        return db_crud.get_watchlist_movies(db, user_email, watched)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/watchlist/watched/movies", response_model=List[WatchlistMovie], summary="Get watched movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_watched_movies(user_email: str, db: Session = Depends(get_db)):
    """
    Returns watched movies from user's watchlist.
    """
    try:
        return db_crud.get_watchlist_watched_movies(db, user_email)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/watchlist/upcoming/movies", response_model=List[WatchlistMovie], summary="Get upcoming movies from user's watchlist", tags=["Watchlists"])
def get_watchlist_upcoming_movies(user_email: str, db: Session = Depends(get_db)):
    """
    Returns upcoming movies from user's watchlist.
    """
    try:
        return db_crud.get_watchlist_upcoming_movies(db, user_email)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")

@moviesWatchListAPI.get("/v1/watchlist/movies/{movie_id}", response_model=WatchlistMovie, summary="Get a movie from user's watchlist", tags=["Watchlists"])
def get_watchlist_movie(movie_id: int, user_email: str, db: Session = Depends(get_db)):
    """
    Returns a movie from user's watchlist.
    """
    try:
        return db_crud.get_watchlist_movie(db, movie_id, user_email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.delete("/v1/watchlist/movies/{movie_id}", summary="Remove a movie from user's watchlist", tags=["Watchlists"])
def remove_watchlist_movie(movie_id: int, user_email: str, db: Session = Depends(get_db)):
    """
    Returns movies from user's watchlist.
    """
    try:
        db_crud.remove_movie_from_watchlist(
            db, movie_id=movie_id, user_email=user_email)
        return {"result": f"Movie with ID {movie_id} has been removed from your watchlist."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


@moviesWatchListAPI.put("/v1/watchlist/movies/{movie_id}/watch", response_model=WatchlistMovie, summary="Mark a movie from user's watchlist as watched", tags=["Watchlists"])
def watch_movie(movie_id: int, user_email: str, db: Session = Depends(get_db)):
    """
    Marks a movie from user's watchlist
    as watched
    """
    try:
        return db_crud.watch_movie(db, movie_id, user_email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    except db_crud.TooSoonException as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occured. Report this message to support: {e}")


if __name__ == '__main__':
    uvicorn.run(moviesWatchListAPI, host="0.0.0.0", port=9999)
