
import json
import re
from http import HTTPStatus
from typing import Dict, List, Optional, Union, Any
from requests import Response
import allure
import pytest
import requests
import random


BASE_URL = "http://localhost:8080/api/v1"
TIMEOUT = 10
RANDOM_ID = random.randint(15, 23)
RANDOM_LARGE_ID = random.randint(60000, 80000)
RANDOM_NEGATIVE_ID = random.randint(-22, -1)
book = {"title": "Introduction to Prompt Engineering", "author": "Onwumere Okechukwu Bright", "category": "Science", "rating": 5}
VALID_PARAMS_TITLE = {"title": "Divergent"}
VALID_PARAMS_TITLE_TWO = {"title": "The Lord of the Rings"}
MULTIPLE_PARAMS_TITLE = {"title": "The Da Vinci Code"}
INVALID_PARAMS_TITLE = {"title": "BadBookTitle"}
EXPECTED_DETAIL = "Book(s) with title 'BadBookTitle' not found"
EXPECTED_DETAIL_MULTIPLE = "Multiple books found"
EXPECTED_DETAIL_INVALID_ID = "Invalid ID: Id must be greater than 0"

test_cases = {
    "GET": [
        # ---------------- All Books ----------------
        {"story": "Get All Books", "endpoint": "/books", "params": None, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": "books", "type": "Positive Test"},
        # ---------------- Books by ID ----------------
        {"story": "Get Books By ID", "endpoint": "/books/6", "params": None, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": None, "type": "Positive Test"},
        {"story": "Get Books By ID", "endpoint": f"/books/{RANDOM_LARGE_ID}", "params": None, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": f"Book with id {RANDOM_LARGE_ID} not found", "check_field": None, "type": "Negative Test"},
        {"story": "Get Books By ID", "endpoint": f"/books/{RANDOM_NEGATIVE_ID}", "params": None, "expected_status": HTTPStatus.BAD_REQUEST, "expected_detail": EXPECTED_DETAIL_INVALID_ID, "check_field": None, "type": "Negative Test"},
        # ---------------- Books by Category ----------------
        {"story": "Get Books By Category", "endpoint": "/books", "params": {"category": "Fantasy"}, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": "category", "type": "Positive Test"},
        {"story": "Get Books By Category", "endpoint": "/books", "params": {"category": "History"}, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": "No books found", "check_field": None, "type": "Negative Test"},
        # ---------------- Books by Title ----------------
        {"story": "Get Books By Title", "endpoint": "/books", "params": MULTIPLE_PARAMS_TITLE, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": "title", "type": "Positive Test"},
        {"story": "Get Books By Title", "endpoint": "/books", "params": {"title": "Sunflower"}, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": None, "check_field": None, "type": "Negative Test"},
    ],
    "DELETE": [
        # ---------------- Delete Book by ID ----------------
        {"story": "Delete Book By ID", "endpoint": "/books/6", "params": None, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": None, "type": "Positive Test"},
        {"story": "Delete Book By ID", "endpoint": f"/books/{RANDOM_LARGE_ID}", "params": None, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": f"Book with id: '{RANDOM_LARGE_ID}' not found", "check_field": None, "type": "Negative Test"},
        {"story": "Delete Book By ID", "endpoint": f"/books/{RANDOM_NEGATIVE_ID}", "params": None, "expected_status": HTTPStatus.BAD_REQUEST, "expected_detail": EXPECTED_DETAIL_INVALID_ID, "check_field": None, "type": "Negative Test"},
        # ---------------- Delete Book by Title ----------------
        {"story": "Delete Book By Title", "endpoint": "/books", "params": VALID_PARAMS_TITLE_TWO, "expected_status": HTTPStatus.OK, "expected_detail": "1 book with title 'Divergent' deleted successfully", "check_field": "category", "type": "Positive Test"},
        {"story": "Delete Book By Title", "endpoint": "/books", "params": INVALID_PARAMS_TITLE, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": EXPECTED_DETAIL, "check_field": None, "type": "Negative Test"}
    ],
    "PUT":[
        # ---------------- Update Book by ID ----------------
        {"story": "Update Book By ID", "endpoint": "/books/4", "params": {}, "payload": book, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": None, "type": "Positive Test"},
        {"story": "Update Book By ID", "endpoint": f"/books/{RANDOM_LARGE_ID}", "params":{}, "payload": book, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": f"Book with id: '{RANDOM_LARGE_ID}' not found", "check_field": None, "type": "Negative Test"},
        {"story": "Update Book By ID", "endpoint": f"/books/{RANDOM_NEGATIVE_ID}", "params":{}, "payload": book, "expected_status": HTTPStatus.BAD_REQUEST, "expected_detail": EXPECTED_DETAIL_INVALID_ID, "check_field": None, "type": "Negative Test"},
        # ---------------- Update Book by Title ----------------
        {"story": "Update Book By Title", "endpoint": "/books", "payload": book, "params": VALID_PARAMS_TITLE, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": "category", "type": "Positive Test"},
        {"story": "Update Book By Title", "endpoint": "/books", "payload": book, "params": INVALID_PARAMS_TITLE, "expected_status": HTTPStatus.NOT_FOUND, "expected_detail": EXPECTED_DETAIL, "check_field": None, "type": "Negative Test"},
        {"story": "Update Book By Title", "endpoint": "/books", "payload": book, "params": MULTIPLE_PARAMS_TITLE, "expected_status": HTTPStatus.CONFLICT, "expected_detail": "Multiple books found", "check_field": None, "type": "Negative Test"}
    ],
    "RECOMMEND":[
        # ---------------- Recommend Book by ID ----------------
        {"story": "Recommend Book By Title", "endpoint": f"/recommendations/{RANDOM_ID}", "params": {}, "payload": {}, "expected_status": HTTPStatus.OK, "expected_detail": None, "check_field": None, "type": "Positive Test"}
    ]
}

def print_response(response):
    print(json.dumps(response.json(), indent=4, sort_keys=True))


def _are_all_strings(params: Dict) -> bool:
    """Check if all keys and values in params are strings.
    Args:
        params: Dictionary to validate
    Returns:
        bool: True if all keys and values are strings, False otherwise
    """
    return all(isinstance(k, str) and isinstance(v, str) 
              for k, v in params.items())


def _validate_request_params(params: Optional[Dict]):
    """Validate request parameters.
    
    Args:
        params: Query parameters to validate
        
    Raises:
        TypeError: If params is not a dict
        ValueError: If params contains non-string keys/values
    """
    if params is None:
        return
        
    if not isinstance(params, dict):
        raise TypeError(f"params must be a dict, got {type(params).__name__}")
    
    if not _are_all_strings(params):
        raise ValueError("All keys and values in params must be strings")


def _validate_positive_response(data: List[Dict], case: Dict[str, Any]):
    """Validate response data for positive test cases.
    
    Args:
        data: List of books from the response
        case: Test case dictionary
    """
    if not case["check_field"] or not case["params"]:
        return
        
    field = next((f for f in ["category", "title"] if f in case["params"]), None)
    if field:
        for book in data:
            assert book[field] == case["params"][field], f"Book {field} mismatch for {case}"


def assign_severity(case: Dict, feature: str) -> tuple:
    """Assign severity level based on test case type."""
    is_positive_test = case["type"] == "Positive Test"
    severity = allure.severity_level.NORMAL if is_positive_test else allure.severity_level.CRITICAL
    badge = "✅" if case["type"] == "Positive Test" else "❌"

    # Dynamic labels for Allure
    allure.dynamic.feature(feature)
    allure.dynamic.story(case["story"])
    allure.dynamic.severity(severity)

    step_title = (
        f"{badge} {case['type']}: {case['story']} | "
        f"Endpoint={case['endpoint']} | Params={case['params'] or 'None'} | "
        f"Expected Status={case['expected_status'].value}"
    )

    return is_positive_test, step_title


def _validate_negative_response(response: Response, case: Dict[str, Any]):
    """Validate response for negative test cases.
    
    Args:
        response: Response object
        case: Test case dictionary
    """
    if case.get("expected_detail"):
        assert response.json().get("detail") == case["expected_detail"], f"Detail mismatch for {case}"


def make_request(method: str, endpoint: str, params: Optional[Dict] = None, json_data: Optional[Dict] = None) -> requests.Response:
    """
    Makes an HTTP request with proper handling of params and json payloads.

    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint (will be appended to BASE_URL)
        params: Query parameters as a dict, or None
        json_data: JSON payload as a dict, or None

    Returns:
        requests.Response object
    """
    _validate_request_params(params)
    
    if json_data is not None and not isinstance(json_data, dict):
        raise TypeError(f"json_data must be a dict, got {type(json_data).__name__}")

    url = f"{BASE_URL}{endpoint}"
    
    try:
        request_kwargs = {
            'method': method,
            'url': url,
            'params': params or {},
            'timeout': TIMEOUT
        }
        
        # Only add json payload for non-GET/DELETE methods
        if method.upper() not in ('GET', 'DELETE'):
            request_kwargs['json'] = json_data or {}
            
        response = requests.request(**request_kwargs)
        print_response(response)
        return response
        
    except Exception as e:
        print(f"Error making {method} request to {url}: {str(e)}")
        raise


def _validate_negative_response_detail(response: requests.Response, case: Dict):
    """Helper to validate error details in negative test cases."""
    if not case:
        return

    response_data = response.json()
    assert response_data.get("detail") == case, f"Expected detail: {case}, Actual: {response_data.get('detail')}"

def _validate_status_code(response: requests.Response, case: Dict):
    """Helper to validate error details in negative test cases."""
    actual_status = response.status_code
    assert actual_status == case, (
        f"Unexpected status code for {case['story']} | "
        f"Expected: {case['expected_status'].value}, Actual: {actual_status}"
    )

def _validate_positive_response_detail(response: requests.Response, case: Dict):
    """Helper to validate error details in negative test cases."""
    # Validate data for positive responses
    books_array = response.json().get("books", [])
    if case:
        value = "category" if "category" in case else "title"
        for data in books_array:
            assert data[value] == case[value], f"Book {value} mismatch for {case}"

def attach_response_body(response: requests.Response):
    allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON
        )

# ------------------- GENERIC GET TEST WITH SEVERITY -------------------
@pytest.mark.get
@pytest.mark.parametrize("case", test_cases["GET"])
def test_generic_get_books_severity(case):
    """
    Generic GET test for Books API with dynamic Allure labels and severity.
    """

    is_positive_test, step_title = assign_severity(case, "Get Books")

    with allure.step(step_title):
        response = make_request("GET", case["endpoint"], params=case["params"])
        _validate_status_code(response, case["expected_status"])

        # Validate data for positive responses
        if is_positive_test and case["check_field"]:
            _validate_positive_response_detail(response, case["params"])
        else:
            # Validate expected detail for negative responses
            _validate_negative_response_detail(response, case["expected_detail"])

        attach_response_body(response)



# ------------------- CREATE BOOK -------------------
@allure.feature('Create Books')
@allure.story('POST /books')
@pytest.mark.create
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


# Define constraints for each field
invalid_rules = {
    "rating": {
        "type": int,
        "invalid_values": [0, 6, 10],  # outside valid range 1-5
        "error_msg": "Invalid rating: Rating must be between 1 and 5"
    },
    "author": {
        "type": str,
        "invalid_values": ["short", "a"*50],  # too short / too long
        "error_msg": "Author must be between 10 and 25 characters"
    },
    "category": {
        "type": str,
        "invalid_values": ["cat", "a"*50],  # too short / too long
        "error_msg": "Category must be between 5 and 20 characters"
    },
    "title_exists": {  # special case for conflict
        "book": {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Fiction", "rating": 4},
        "status": HTTPStatus.CONFLICT.value,
        "error_msg": "Book already exists"
    }
}

# Generate all parameterized test cases dynamically
parametrize_data = []

# Add invalid field cases
for field, rules in invalid_rules.items():
    if field == "title_exists":
        parametrize_data.append((rules["book"], rules["status"], rules["error_msg"]))
        continue
    base_book = {"title": "The Great Summer", "author": "Valid Author", "category": "Fiction", "rating": 4}
    for invalid_value in rules["invalid_values"]:
        book = base_book.copy()
        book[field] = invalid_value
        parametrize_data.append((book, HTTPStatus.BAD_REQUEST.value, rules["error_msg"]))

@allure.feature('Create Books')
@pytest.mark.create
@pytest.mark.parametrize("book, expected_status, expected_detail", parametrize_data)
def test_negative_create_book_dynamic(book, expected_status, expected_detail):
    """ Dynamically generated negative tests for creating a book """
    response = make_request("POST", "/books", json_data=book)
    response_json = response.json()
    assert response_json['status'] == expected_status
    assert response_json['detail'] == expected_detail


# ------------------- GENERIC UPDATE BOOK TEST WITH SEVERITY -------------------
@pytest.mark.put
@pytest.mark.parametrize("case", test_cases["PUT"])
def test_generic_update_books_severity(case):
    """
    Generic UPDATE test for Books API with dynamic Allure labels and severity.
    pytest -m put
    """
    is_positive_test, step_title = assign_severity(case, "Update Books")

    with allure.step(step_title):
        response = make_request("PUT", case["endpoint"], json_data=case["payload"], params=case["params"])
        _validate_status_code(response, case["expected_status"])

        # Validate data for positive responses
        if is_positive_test and case["check_field"]:
            _validate_positive_response_detail(response, case["params"])
        else:
            # Validate expected detail for negative responses
            _validate_negative_response_detail(response, case["expected_detail"])

        attach_response_body(response)


# ------------------- GENERIC DELETE BOOK TEST WITH SEVERITY -------------------
@pytest.mark.get
@pytest.mark.parametrize("case", test_cases["DELETE"])
def test_generic_delete_books_severity(case):
    """
    Generic DELETE test for Books API with dynamic Allure labels and severity.
    """
    is_positive_test, step_title = assign_severity(case, "Delete Books")

    with allure.step(step_title):
        response = make_request("DELETE", case["endpoint"], params=case["params"])
        _validate_status_code(response, case["expected_status"])

        # Validate data for positive responses
        if is_positive_test and case["check_field"]:
            _validate_positive_response_detail(response, case["params"])
        else:
            # Validate expected detail for negative responses
            _validate_negative_response_detail(response, case["expected_detail"])

        attach_response_body(response)


@pytest.mark.recommend
@pytest.mark.parametrize("case", test_cases["RECOMMEND"])
def test_recommendations(case):
    _, step_title = assign_severity(case, "Recommend Books")

    with allure.step(step_title):
        response = make_request("GET", case["endpoint"], params=case["params"])
        _validate_status_code(response, case["expected_status"])
        response_json = response.json()
        recommendations = response_json.get("recommendations", [])
        assert isinstance(recommendations, list), f"Expected list, got {type(recommendations)}"
        assert len(recommendations) == 5
        assert all(isinstance(novel, str) for novel in recommendations)

        attach_response_body(response)


