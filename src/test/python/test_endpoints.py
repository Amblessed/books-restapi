
import requests
import re
import allure
import json
from http import HTTPStatus


BASE_URL = "http://localhost:8080/api/v1"
TIMEOUT = 10

def print_response(response):
    print(json.dumps(response.json(), indent=4, sort_keys=True))

def make_request(method, endpoint, params=None, json_data=None):
    """
    Makes an HTTP request with proper handling of params and json payloads.
    """
    url = f"{BASE_URL}{endpoint}"
    # Only include json if json_data is provided
    request_kwargs = {"timeout": TIMEOUT}
    if params:
        request_kwargs["params"] = params
    if json_data:
        request_kwargs["json"] = json_data

    response = requests.request(method, url, **request_kwargs)
    print_response(response)
    return response

# ------------------- GET BOOKS -------------------
@allure.feature('Get Books')
@allure.story('GET /books')
def test_get_books():
    """Test GET Books"""
    response = make_request("GET", "/books")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['books']) > 0

# ------------------- GET BOOKS BY ID -------------------
@allure.feature('Get Books By ID')
@allure.story('Positive Test: Valid ID')
def test_positive_get_books_by_id_valid_id():
    """
    Test GET Books By Category: Positive Test

    """
    user_id = 6
    response = make_request("GET", f"/books/{user_id}")
    assert response.status_code == HTTPStatus.OK


@allure.feature('Get Books By ID')
@allure.story('Negative Test: Invalid ID')
def test_negative_get_books_by_id_invalid_id():
    """
    Test GET Books By ID
    """
    user_id = 4999
    response = make_request("GET", f"/books/{user_id}")
    assert response.json()['status'] == HTTPStatus.NOT_FOUND.value
    assert response.json()['detail'] == f"Book with id {user_id} not found"

@allure.feature('Get Books By ID')
@allure.story('Negative Test: Negative ID')
def test_negative_get_books_by_id_negative_id():
    """
    Test GET Books By ID
    """
    user_id = -5
    response = make_request("GET", f"/books/{user_id}")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == "Invalid ID: Id must be greater than 0"


# ------------------- GET BOOKS BY CATEGORY -------------------
@allure.feature('Get Books By Category')
@allure.story('Positive Test: Valid Category')
def test_positive_get_books_by_category():
    """
    Test GET Books By Category: Positive Test
    params = {'category': 'Fantasy'}
    """
    params = {'category': 'Fantasy'}
    response = make_request("GET", "/books", params=params)
    assert response.status_code == HTTPStatus.OK
    for book in response.json()['books']:
        assert book['category'] == 'Fantasy'

@allure.feature('Get Books By Category')
@allure.story('Negative Test: Category Not Found')
def test_negative_get_books_by_category():
    """
    Test GET Books By Category
    params = {'category': 'History'}
    """
    params = {'category': 'History'}
    response = make_request("GET", "/books", params=params)
    assert response.json()['status'] == HTTPStatus.NOT_FOUND.value
    assert response.json()['detail'] == "No books found"

# ------------------- GET BOOK BY TITLE -------------------
@allure.feature('Get Books By Title')
@allure.story('Positive Test: Valid Title')
def test_positive_get_book_by_title():
    """Test GET Books"""
    params = {'title': 'The Da Vinci Code'}
    response = make_request("GET", "/books", params=params)
    assert response.status_code == HTTPStatus.OK
    for book in response.json()['books']:
        assert book['title'] == 'The Da Vinci Code'

@allure.feature('Get Books By Title')
@allure.story('Negative Test: Invalid Title')
def test_negative_get_book_by_title():
    """
    Test GET Book By Title with Unknown Title
    """
    params = {'title': 'Sunflower'}
    response = make_request("GET","/books", params=params)
    assert response.status_code == HTTPStatus.NOT_FOUND


# ------------------- CREATE BOOK -------------------
@allure.feature('Create Books')
@allure.story('POST /books')
def test_positive_create_book_valid_parameters():
    """Test Create Book with new Title"""
    book = {
        "title": "The Rebound",
        "author": "Peter Johnson",
        "category": "Classic",
        "rating": 5
    }

    response = make_request("POST", "/books", json_data=book)
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json['message'] == "Book created successfully"
    response_json_body = response_json['book']
    assert response_json_body['title'] == book['title']
    assert response_json_body['author'] == book['author']
    assert response_json_body['category'] == book['category']
    assert response_json_body['rating'] == book['rating']


@allure.feature('Create Books')
@allure.story('Negative Test: Book Already Exists')
def test_negative_create_book_exist_title():
    """ Test Create Book with already existing title """
    book = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Fiction",
        "rating": 4
    }
    response = make_request("POST", "/books", json_data=book)
    response_json = response.json()
    assert response_json['status'] == HTTPStatus.CONFLICT.value
    assert response_json['detail'] == "Book already exists"

@allure.feature('Create Books')
@allure.story('Negative Test: Create Book with Invalid Rating')
def test_negative_create_book_invalid_rating():
    """ Test Create Book with invalid rating """
    book = {
        "title": "The Great Summer",
        "author": "F. Scott Fitzgerald",
        "category": "Fiction",
        "rating": 6
    }
    response = make_request("POST", "/books", json_data=book)
    response_json = response.json()
    assert response_json['status'] == HTTPStatus.BAD_REQUEST.value
    assert response_json['detail'] == "Invalid rating: Rating must be between 1 and 5"

@allure.feature('Create Books')
@allure.story('Negative Test: Create Book with Invalid Author')
def test_negative_create_book_invalid_author():
    """ Test Create Book with invalid author """
    """Test Create Book with invalid author lengths."""
    book = {"title": "The Great Summer", "category": "Fiction", "rating": 4}
    invalid_authors = [
        "the",  # too short
        "thegjjksdgjgskjdfgkhjdhskjbgdkjfbgjdfbgsjdbfjkfjdbvdfjbjfbjfbjfbfjbfbjs"  # too long
    ]

    for author in invalid_authors:
        book["author"] = author
        response = make_request("POST", "/books", json_data=book)
        response_json = response.json()
        assert response_json['status'] == HTTPStatus.BAD_REQUEST.value
        assert response_json['detail'] == "Author must be between 10 and 25 characters"

@allure.feature('Create Books')
@allure.story('Negative Test: Create Book with Invalid Category')
def test_negative_create_book_invalid_category():
    """ Test Create Book with invalid category """
    book = {"title": "The Great Summer", "author": "James Peterson", "rating": 4}
    invalid_categories = [
        "ft",  # too short
        "Introduction to Programming for Beginners"  # too long
    ]

    for category in invalid_categories:
        book["category"] = category
        response = make_request("POST", "/books", json_data=book)
        response_json = response.json()
        assert response_json['status'] == HTTPStatus.BAD_REQUEST.value
        assert response_json['detail'] == "Category must be between 5 and 20 characters"


# ------------------- UPDATE BOOK -------------------
@allure.feature('Update Book By ID')
@allure.story('Positive Test: Valid ID')
def test_positive_update_book_by_id_valid_id():
    """Test Update Book with new Values"""
    update_id = 4
    book = {"title": "Introduction to Prompt Engineering", "author": "Onwumere Okechukwu Bright", "category": "Science", "rating": 5}
    response = make_request("PUT", f"/books/{update_id}", json_data=book)
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == "Book updated successfully"
    assert response.json()['UpdatedBook']['title'] == book['title']
    assert response.json()['UpdatedBook']['author'] == book['author']
    assert response.json()['UpdatedBook']['category'] == book['category']
    assert response.json()['UpdatedBook']['rating'] == book['rating']

@allure.feature('Update Book By ID')
@allure.story('Negative Test: Invalid ID')
def test_negative_update_book_by_id_invalid_id():
    """Test Update Book with new Values"""
    update_id = 100
    book = {
        "title": "Introduction to Python",
        "author": "Onwumere Okechukwu Bright",
        "category": "Computer Science",
        "rating": 5
    }
    response = make_request("PUT", f"/books/{update_id}", json_data=book)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == f"Book with id: '{update_id}' not found"

@allure.feature('Update Book By Title')
@allure.story('Positive Test: Valid Title')
def test_positive_update_book_by_title_valid_title():
    """Test Update Book by Title with new Values"""
    params = {'title': 'The Great Gatsby'}
    book = {
        "title": "Introduction to OpenAI API",
        "author": "Onwumere Okechukwu Bright",
        "category": "Science",
        "rating": 5
    }
    response = make_request("PUT", "/books", params=params, json_data=book)
    assert response.status_code == HTTPStatus.OK

@allure.feature('Update Book By Title')
@allure.story('Negative Test: Invalid Title')
def test_negative_update_book_invalid_title():
    """Test Update Book with new Values"""
    params = {'title': 'Introduction to Computer Science'}
    book = {
        "title": "Introduction to Python",
        "author": "Onwumere Okechukwu Bright",
        "category": "Computer Science",
        "rating": 5
    }
    response = make_request("PUT", "/books", params=params, json_data=book)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == "Book not found"

@allure.feature('Update Book By Title')
@allure.story('Negative Test: Multiple Books Found')
def test_negative_update_book_multiple_books_found():
    """Test Update Book with new Values"""

    params = {'title': 'The Da Vinci Code'}
    book = {
        "title": "Introduction to Generative AI",
        "author": "Onwumere Okechukwu Bright",
        "category": "Science",
        "rating": 5
    }
    response = make_request("PUT", "/books", params=params, json_data=book)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['message'] == "Multiple books found"


# ------------------- DELETE BOOK -------------------
@allure.feature('Delete Book By ID')
@allure.story('Positive Test: Valid ID')
def test_positive_delete_book_by_id_valid_id():
    """
    Test Delete Book with existing ID:
    """
    user_id = 11
    response = make_request("DELETE", f"/books/{user_id}")
    assert response.status_code == HTTPStatus.OK

@allure.feature('Delete Book By ID')
@allure.story('Negative Test: Invalid ID')
def test_negative_delete_book_by_id_invalid_id():
    """
    Test Delete Book with invalid ID:
    """
    user_id = 99999999
    response = make_request("DELETE", f"/books/{user_id}")
    assert response.json()['status'] == HTTPStatus.NOT_FOUND.value
    assert response.json()['detail'] == f"Book with id: '{user_id}' not found"

@allure.feature('Delete Book By Title')
@allure.story('Positive Test: Valid Title')
def test_positive_delete_book_by_title_valid_title():
    """
    Test Delete Book with existing title:
    title = 'The Hobbit'
    """
    params = {'title': 'Divergent'}
    response = make_request("DELETE", "/books", params=params)
    assert response.status_code == HTTPStatus.OK

@allure.feature('Delete Book By Title')
@allure.story('Negative Test: Invalid Title')
def test_negative_delete_book_by_title_invalid_title():
    """
    Test Delete Book with unknown title:
    title = 'Introduction to Accounting'
    """
    params = {'title': 'Introduction to Accounting'}
    response = make_request("DELETE", "/books", params=params)
    assert response.json()['status'] == HTTPStatus.NOT_FOUND.value
    assert response.json()['detail'] == f"Book(s) with title '{params['title']}' not found"