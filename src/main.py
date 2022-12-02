import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import db_models
import database_crud as db_crud
import authentication as auth
from database import engine
from schemas import UserSignUp, User, Movie, MovieDetails, WatchlistInput, Watchlist, WatchlistMovie, Token
from typing import List
from routers import users, movies, watchlists

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

db_models.Base.metadata.create_all(bind=engine)

moviesWatchListAPI.add_middleware(CORSMiddleware, allow_origins=['*'])

moviesWatchListAPI.include_router(users.router)
moviesWatchListAPI.include_router(movies.router)
moviesWatchListAPI.include_router(watchlists.router)


if __name__ == '__main__':
    uvicorn.run(moviesWatchListAPI, host="0.0.0.0", port=9999)
