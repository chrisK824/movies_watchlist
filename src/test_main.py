import json
from random import randint
from datetime import datetime
from fastapi.testclient import TestClient
from random_word import RandomWords
from main import moviesWatchListAPI
from datetime import datetime
from schemas import MovieDetails

client = TestClient(moviesWatchListAPI)

def test_get_movies():
    response = client.get(f"/v1/movies")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert isinstance(movie, MovieDetails)

def get_watched_movies():
    response = client.get(f"/v1/movies/watched")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert isinstance(movie, MovieDetails)
        assert movie['watched'] == True

def get_upcoming_movies():
    response = client.get(f"/v1/movies/upcoming")
    assert response.status_code == 200
    assert type(response.json()) == list
    for movie in response.json():
        assert isinstance(movie, MovieDetails)
        assert datetime.strptime(movie['release_date'], '%d-%m-%y')  > datetime.utcnow()

def test_post_movie():
    ref_book_id = randint(1,10)
    ref_body = {
        "title" : RandomWords().get_random_word(),
        "release_date" : datetime(
            year=randint(1930,2030),
            month=randint(1,12),
            day=randint(1,28)).strftime('%d-%m-%y')
    }
    response = client.post(f"/v1/movies", data=json.dumps(ref_body))
    assert response.status_code == 200
    response = response.json()
    assert isinstance(response, MovieDetails)
    assert response["title"] == ref_body["title"]
    assert response["release_date"] == ref_body["release_date"]

# def test_post_review_fail_missing_book_id():
#     ref_book_id = 0
#     ref_body = {
#         "book_id" : ref_book_id,
#         "rating" : randint(0,5),
#         "review" : RandomWords().get_random_word()
#     }
#     ref_res = {
#         "detail" : f"No book found with ID {ref_book_id}"
#     }
#     print(f"Posting review for non existing book with ID '{ref_book_id}'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 404
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_post_review_fail_missing_rating_field():
#     ref_book_id = randint(1,10)
#     ref_body = {
#         "book_id" : ref_book_id,
#         "review" : RandomWords().get_random_word()
#     }
#     ref_res = {
#         "detail": [
#             {
#             "loc": [
#                 "body",
#                 "rating"
#             ],
#             "msg": "field required",
#             "type": "value_error.missing"
#             }
#         ]
#     }
#     print(f"Posting review with missing field 'rating'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 422
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_post_review_fail_missing_book_id_field():
#     ref_body = {
#         "rating" : randint(0,5),
#         "review" : RandomWords().get_random_word()
#     }
#     ref_res = {
#         "detail": [
#             {
#             "loc": [
#                 "body",
#                 "book_id"
#             ],
#             "msg": "field required",
#             "type": "value_error.missing"
#             }
#         ]
#     }
#     print(f"Posting review with missing field 'book_id'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 422
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_post_review_fail_missing_review_field():
#     ref_book_id = randint(1,10)
#     ref_body = {
#         "book_id" : ref_book_id,
#         "rating" : randint(0,5)
#     }
#     ref_res = {
#         "detail": [
#             {
#             "loc": [
#                 "body",
#                 "review"
#             ],
#             "msg": "field required",
#             "type": "value_error.missing"
#             }
#         ]
#     }
#     print(f"Posting review with missing field 'review'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 422
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_post_review_fail_negative_rating_field():
#     ref_book_id = randint(1,10)
#     ref_body = {
#         "book_id" : ref_book_id,
#         "rating" : -1,
#         "review" : RandomWords().get_random_word()
#     }
#     ref_res = {
#         "detail": [
#             {
#             "loc": [
#                 "body",
#                 "rating"
#             ],
#             "msg": "ensure this value is greater than or equal to 0",
#             "type": "value_error.number.not_ge",
#             "ctx": {
#                 "limit_value": 0
#             }
#             }
#         ]
#     }
#     print(f"Posting review with wrong negative integer for field 'rating'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 422
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_post_review_fail_positive_rating_field():
#     ref_book_id = randint(1,10)
#     ref_body = {
#         "book_id" : ref_book_id,
#         "rating" : 6,
#         "review" : RandomWords().get_random_word()
#     }
#     ref_res = {
#         "detail": [
#             {
#             "loc": [
#                 "body",
#                 "rating"
#             ],
#             "msg": "ensure this value is less than or equal to 5",
#             "type": "value_error.number.not_le",
#             "ctx": {
#                 "limit_value": 5
#             }
#             }
#         ]
#     }
#     print(f"Posting review with wrong positive integer for field 'rating'")
#     response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#     assert response.status_code == 422
#     response = response.json()
#     assert isinstance(response, dict)
#     assert response == ref_res

# def test_top_n_rated_books():
#     books_number = 3
#     for i in range(50):
#         ref_book_id = randint(1,10)
#         ref_body = {
#             "book_id" : ref_book_id,
#             "rating" : 5,
#             "review" : RandomWords().get_random_word()
#         }
#         ref_res = {
#             "result": f"Review posted successfully for book {ref_book_id}"
#         }
#         print(f"Posting review for book with ID '{ref_book_id}' with rating 5")
#         response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#         assert response.status_code == 200
#         assert ref_res == response.json()
#     response = client.get(f"/v1/reviews/top?books_number={books_number}")
#     assert response.status_code == 200
#     res = response.json()
#     assert len(res["books"]) == 3
#     print(f"Retrieved top 3 rated books:")
#     print(json.dumps(res, indent=4))

# def get_current_month_avg_rating(ref_book_id):
#     # get average rating of current month
#     current_month = datetime.now().strftime("%B")
#     response = client.get(f"/v1/reviews/monthly?book_id={ref_book_id}")
#     assert response.status_code == 200
#     current_month_avg_rating = response.json()["result"]["average_ratings"][current_month]
#     return {current_month : current_month_avg_rating}

# def create_avg_rating_for_current_month(book_id, reviews_number):
#     # post reviews_number random reviews with random ratings
#     # initiate sum of reviews
#     ratings_sum = 0
#     for i in range(reviews_number):
#         # rating = randint(0,5)
#         rating = 4
#         ref_body = {
#             "book_id" : book_id,
#             "rating" : rating,
#             "review" : RandomWords().get_random_word()
#         }
#         ref_res = {
#             "result": f"Review posted successfully for book {book_id}"
#         }
#         print(f"Posting review for book with ID '{book_id}' with rating '{rating}'")
#         response = client.post(f"/v1/reviews", data=json.dumps(ref_body))
#         assert response.status_code == 200
#         assert ref_res == response.json()
#         ratings_sum = ratings_sum + rating
#     ref_avg_rating = ratings_sum/reviews_number
#     return ref_avg_rating

# def test_monthly_average_rating():
#     ref_book_id = 500
#     reviews_number = 10
#     current_month_avg_rating_dict = get_current_month_avg_rating(ref_book_id)
#     current_month = list(current_month_avg_rating_dict.keys())[0]
#     current_month_avg_rating = current_month_avg_rating_dict[current_month]
#     print(f"Average rating for {current_month} : {current_month_avg_rating}, already in db")
#     created_avg_rating_for_curr_month = create_avg_rating_for_current_month(ref_book_id, reviews_number)
#     print(f"Average rating for {current_month} : {created_avg_rating_for_curr_month}, created from simulated input")
#     if current_month_avg_rating is not None:
#         ref_avg_rating = round((current_month_avg_rating + created_avg_rating_for_curr_month)/2, 2)
#     else:
#         ref_avg_rating = round(created_avg_rating_for_curr_month, 2)
#     ref_res = {
#         "result": {
#             "book_id": ref_book_id,
#             "average_ratings": {
#                 "January": None,
#                 "February": None,
#                 "March": None,
#                 "April": None,
#                 "May": None,
#                 "June": None,
#                 "July": None,
#                 "August": None,
#                 "September": None,
#                 "October": None,
#                 "November": None,
#                 "December": None
#             }
#         }
#     }
#     for month, _ in ref_res["result"]["average_ratings"].items():
#         if month == current_month:
#             ref_res["result"]["average_ratings"][month] = ref_avg_rating
#             break
#     print(f"Reference monthly average ratings for book with ID '{ref_book_id}'")
#     print(json.dumps(ref_res, indent=4))
#     print(f"Retrieving monthly average ratings for book with ID '{ref_book_id}'")
#     response = client.get(f"/v1/reviews/monthly?book_id={ref_book_id}")
#     print(json.dumps(response.json(), indent=4))
#     assert response.status_code == 200
#     assert ref_res == response.json()