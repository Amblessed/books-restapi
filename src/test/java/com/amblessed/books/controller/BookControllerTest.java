package com.amblessed.books.controller;

/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 06-Sep-25
 */

import static org.hamcrest.number.OrderingComparison.greaterThan;
import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.amblessed.books.entity.Book;
import com.amblessed.books.entity.BookRequest;
import com.amblessed.books.exception.BookNotFoundException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;

import java.util.List;
import java.util.Map;


@WebMvcTest(BookController.class)
@ExtendWith(MockitoExtension.class)
@AutoConfigureMockMvc(addFilters = false)
class BookControllerTest {

    @InjectMocks
    private BookController bookController;

    @Autowired
    private MockMvc mockMvc;
    private final ObjectMapper objectMapper = new ObjectMapper();


    // Helper method for MockMvc GET requests
    private ResultActions performGet(String url, Map<String, String> params) throws Exception {
        MockHttpServletRequestBuilder request = get(url).accept(MediaType.APPLICATION_JSON);
        if (params != null) {
            params.forEach(request::param);
        }
        return mockMvc.perform(request);
    }

    private ResultActions performJsonRequest(HttpMethod method, String url, Object body, Map<String, String> params) throws Exception {
        MockHttpServletRequestBuilder request;
        if (method == HttpMethod.POST) {
            request = post(url);
        } else if (method == HttpMethod.PUT) {
            request = put(url);
        } else if (method == HttpMethod.DELETE) {
            request = delete(url);
        } else {
            throw new IllegalArgumentException("Unsupported method: " + method);
        }
        if (params != null) params.forEach(request::param);

        if (body != null) {
            request.contentType(MediaType.APPLICATION_JSON)
                    .content(objectMapper.writeValueAsString(body));
        }
        return mockMvc.perform(request);
    }

    @Test
    @DisplayName("Get all books returns JSON array")
    void givenBooks_whenGetBooks_thenReturnJsonArray() throws Exception {
        performGet("/api/v1/books", null)
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.books").exists())
                .andExpect(jsonPath("$.books.length()").value(greaterThan(0)));
    }

    @Test
    @DisplayName("Get book by title returns book")
    void givenBookTitle_whenGetBookByTitle_thenReturnBook() throws Exception {
        performGet("/api/v1/books", Map.of("title", "1984"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.books[0].title").value("1984"));
    }

    @Test
    @DisplayName("Get book by unknown title returns 404")
    void givenUnknownBookTitle_whenGetBookByTitle_thenReturnNotFound() throws Exception {
        performGet("/api/v1/books", Map.of("title", "Unknown Book"))
                .andExpect(status().isNotFound());
    }

    @Test
    void givenUnknownCategoryOrAuthorOrTitle_whenGetBooks_thenReturnNotFound() throws Exception {
        performGet("/api/v1/books", Map.of("category", "Nonexistent Category"))
                .andExpect(status().isNotFound());

        performGet("/api/v1/books", Map.of("author", "Ghost Author"))
                .andExpect(status().isNotFound());

        performGet("/api/v1/books", Map.of("title", "Unknown Book"))
                .andExpect(status().isNotFound());

        performGet("/api/v1/books", Map.of(
                "title", "Unknown Book",
                "category", "Nonexistent Category",
                "author", "Ghost Author"))
                .andExpect(status().isNotFound());
    }

    // Controller unit tests using mocks
    @Test
    void testGetBookById() throws Exception {
        performGet("/api/v1/books/1", null)
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.book.title").value("To Kill a Mockingbird"));
    }

    @Test
    void testGetBooks() throws Exception {
        performGet("/api/v1/books", null)
                .andExpect(status().isOk())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.books.length()").value(16))
                .andExpect(jsonPath("$.books[0].title").value("To Kill a Mockingbird"));
    }

    @Test
    void testCreateBook() throws Exception {
        BookRequest request = new BookRequest("Introduction to Computer Architecture", "Onwumere Okey", "Science", 5);
        performJsonRequest(HttpMethod.POST, "/api/v1/books", request, null)
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.message").value("Book created successfully"))
                .andExpect(jsonPath("$.book.title").value("Introduction to Computer Architecture"));
    }

    @Test
    void testUpdateBook() throws Exception {
        BookRequest request = new BookRequest("To Kill a Mockingbird", "Harper Lee", "Fiction", 5);
        performJsonRequest(HttpMethod.PUT, "/api/v1/books", request, Map.of("title", "To Kill a Mockingbird"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Book updated successfully"));
    }

    @Test
    void testUpdateBookById() throws Exception {
        long bookId = 1L;
        BookRequest request = new BookRequest("To Kill a Mockingbird", "Harper Lee", "Fiction", 5);

        performJsonRequest(HttpMethod.PUT, "/api/v1/books/" + bookId, request, null)
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Book updated successfully"))
                .andExpect(jsonPath("$.UpdatedBook.title").value("To Kill a Mockingbird"))
                .andExpect(jsonPath("$.UpdatedBook.author").value("Harper Lee"))
                .andExpect(jsonPath("$.UpdatedBook.category").value("Fiction"))
                .andExpect(jsonPath("$.UpdatedBook.rating").value(5));
    }

    @Test
    void testDeleteBookByTitle() throws Exception {
        performJsonRequest(HttpMethod.DELETE, "/api/v1/books", null,
                Map.of("title", "To Kill a Mockingbird"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("1 book with title 'To Kill a Mockingbird' deleted successfully"));
    }

    @Test
    void testDeleteBookByIdPositiveTest() throws Exception {
        performJsonRequest(HttpMethod.DELETE, "/api/v1/books/1", null, null)
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Book with id: '1' deleted successfully"));
    }

    @Test
    void testDeleteBookByIdNegativeTest() throws Exception {
        long nonExistentId = 999_999_999L;

        performJsonRequest(HttpMethod.DELETE, "/api/v1/books/" + nonExistentId, null, null)
                .andExpect(result -> {
                    Exception resolvedException = result.getResolvedException();
                    assertNotNull(resolvedException, "Expected an exception to be thrown");
                    BookNotFoundException ex = assertInstanceOf(BookNotFoundException.class, resolvedException);
                    assertEquals(String.format("Book with id: '%d' not found", nonExistentId), ex.getMessage());
                })
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.detail").value(String.format("Book with id: '%d' not found", nonExistentId)));
    }
}