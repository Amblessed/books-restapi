# Books REST API

[![CI](https://github.com/amblessed/booksapi/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/amblessed/booksapi/actions/workflows/ci.yml)


[![Allure Report](https://img.shields.io/badge/Allure-Report-ED5C5C?logo=allure&logoColor=white)](https://amblessed.github.io/booksapi/)


This project is a Spring Boot application that provides a REST API for managing books. The application provides several endpoints for performing CRUD operations on books. The API testing was done using Python requests library with pytest framework.

## Features

| HTTP Method | Endpoint    | Description                                                                                                        |
| ----------- | ----------- | ------------------------------------------------------------------------------------------------------------------ |
| GET         | /books      | Retrieve books. Accepts query parameters: `title`, `author`, `category`. Any combination of parameters is allowed. |
| POST        | /books      | Create a new book.                                                                                                 |
| PUT         | /books      | Update a book by `title` (query parameter only).                                                                   |
| PUT         | /books/{id} | Update a book by ID.                                                                                               |
| DELETE      | /books      | Delete a book by `title` (query parameter only).                                                                   |
| DELETE      | /books/{id} | Delete a book by ID.                                                                                               |


### Notes:

- **GET /books**: Flexible querying. Examples:
   - `/books?title=Book1` → Get by title
   - `/books?author=Author1&category=Fiction` → Get by author and category
   - `/books` → Get all books

- **PUT /books and DELETE /books** by title require exactly one title query parameter.


⚙️ Getting Started
### Prerequisites

- Java 17+
- Maven
- Spring Boot 3
- Python 3+ (for testing)
- Pytest (for testing)

### Installing

1. Clone the repository
```
git clone https://github.com/amblessed/books-api.git
```
2. Navigate to the project directory
```
cd books-api
```
3. Build the project
```
mvn clean install
```
4. Run the application
```
mvn spring-boot:run
```
The application will start and listen on `http://localhost:8080/api/v1`.

🧪 Running Tests

The tests are written in Python using the requests library and pytest framework. To run the tests, run the following command:

```
pytest
```
This would run all the test and open the results in a browser. See `confest.py` for configurations

🛠 Built With

- [Spring Boot](https://spring.io/projects/spring-boot) - The web framework used
- [Maven](https://maven.apache.org/) - Dependency Management
- [Python](https://www.python.org/) - Used for testing
- [Pytest](https://docs.pytest.org/en/latest/) - The testing framework used

👤 Authors
- *Onwumere Okechukwu Bright* - *Initial work* - [Amblessed](https://github.com/amblessed)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
