import json
from random import randint
from datetime import datetime
from fastapi.testclient import TestClient
from random_word import RandomWords
from main import moviesWatchListAPI
from datetime import datetime, timedelta
from schemas import MovieDetails

client = TestClient(moviesWatchListAPI)


def create_movie_by_name(title):
    ref_body = {
        "title": title,
        "release_date": (datetime.now()+timedelta(weeks=randint(-2000, 200))).strftime('%Y-%m-%d')
    }
    response = client.post(f"/v1/movies", data=json.dumps(ref_body))
    ref_id = response.json()['id']
    return ref_id


def create_released_movie():
    ref_body = {
        "title": RandomWords().get_random_word(),
        "release_date": (datetime.now()-timedelta(days=1)).strftime('%Y-%m-%d')
    }
    response = client.post(f"/v1/movies", data=json.dumps(ref_body))
    ref_id = response.json()['id']
    return ref_id


def create_unreleased_movie():
    ref_body = {
        "title": RandomWords().get_random_word(),
        "release_date": (datetime.now()+timedelta(days=1)).strftime('%Y-%m-%d')
    }
    response = client.post(f"/v1/movies", data=json.dumps(ref_body))
    ref_id = response.json()['id']
    return ref_id


def watch_movie():
    ref_id = create_released_movie()
    ref_body = {
        "value": True
    }
    client.put(f"/v1/movies/{ref_id}", data=json.dumps(ref_body))
    return ref_id


def test_post_movie():
    ref_body = {
        "title": RandomWords().get_random_word(),
        "release_date": datetime(
            year=randint(1930, 2030),
            month=randint(1, 12),
            day=randint(1, 28)).strftime('%Y-%m-%d')
    }
    response = client.post(f"/v1/movies", data=json.dumps(ref_body))
    assert response.status_code == 200
    response = response.json()
    assert (response.keys() == MovieDetails.__fields__.keys())
    assert response["title"] == ref_body["title"]
    assert response["release_date"] == ref_body["release_date"]


def test_get_movies():
    create_released_movie()
    create_unreleased_movie()
    response = client.get(f"/v1/movies")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert (movie.keys() == MovieDetails.__fields__.keys())


def test_watch_movie_success():
    ref_id = create_released_movie()
    ref_body = {
        "value": True
    }
    response = client.put(f"/v1/movies/{ref_id}", data=json.dumps(ref_body))
    assert response.status_code == 200
    response = response.json()
    assert (response.keys() == MovieDetails.__fields__.keys())
    assert response["id"] == ref_id
    assert response["watched"] == ref_body["value"]
    assert response["watched_date"] is not None


def test_watch_movie_fail():
    ref_id = create_unreleased_movie()
    ref_body = {
        "value": True
    }
    response = client.put(f"/v1/movies/{ref_id}", data=json.dumps(ref_body))
    assert response.status_code == 403
    response = response.json()
    assert 'detail' in response


def test_watched_movies():
    ref_id = watch_movie()
    response = client.get(f"/v1/movies/watched")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert (movie.keys() == MovieDetails.__fields__.keys())
        assert movie['watched'] == True


def test_upcoming_movies():
    create_unreleased_movie()
    response = client.get(f"/v1/movies/upcoming")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert (movie.keys() == MovieDetails.__fields__.keys())
        assert datetime.strptime(
            movie['release_date'], '%Y-%m-%d') > datetime.utcnow()


def test_search_movies():
    ref_title = "test movie"
    ref_id = create_movie_by_name(ref_title)
    response = client.get(f"/v1/movies/search?keyword={ref_title}")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert (movie.keys() == MovieDetails.__fields__.keys())
        if movie['id'] == ref_id:
            assert movie['title'] == ref_title
