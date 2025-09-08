package com.amblessed.books.controller;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 06-Sep-25
 */

import com.amblessed.books.entity.Book;
import com.amblessed.books.entity.BookRequest;
import com.amblessed.books.exception.BookAlreadyExistsException;
import com.amblessed.books.exception.BookNotFoundException;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@Tag(name = "Books", description = "Books API")
@RestController
@RequestMapping("/api/v1")
public class BookController {

    private final List<Book> books = new ArrayList<>();

    public BookController() {
        initBooks();
    }


    private void initBooks() {
        books.add(new Book(1, "To Kill a Mockingbird", "Harper Lee", "Fiction", 5));
        books.add(new Book(2, "1984", "George Orwell", "Fiction", 4));
        books.add(new Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 4));
        books.add(new Book(4, "The Catcher in the Rye", "J.D. Salinger", "Fiction", 3));
        books.add(new Book(5, "Moby Dick", "Herman Melville", "Fiction", 4));
        books.add(new Book(6, "War and Peace", "Leo Tolstoy", "Fiction", 5));
        books.add(new Book(7, "Pride and Prejudice", "Jane Austen", "Fiction", 4));
        books.add(new Book(8, "The Hobbit", "J.R.R. Tolkien", "Fantasy", 5));
        books.add(new Book(9, "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 5));
        books.add(new Book(10, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 5));
        books.add(new Book(11, "The Da Vinci Code", "Dan Brown", "Thriller", 4));
        books.add(new Book(12, "The Girl with the Dragon Tattoo", "Stieg Larsson", "Thriller", 4));
        books.add(new Book(13, "Gone Girl", "Gillian Flynn", "Thriller", 4));
        books.add(new Book(14, "The Hunger Games", "Suzanne Collins", "Dystopian", 4));
        books.add(new Book(15, "Divergent", "Veronica Roth", "Dystopian", 3));
        books.add(new Book(16, "The Da Vinci Code", "Onwumere Bright", "Thriller", 5));
    }

    @Operation(summary = "Get Book By ID", description = "Get a particular Book By ID")
    @GetMapping("/books/{id}")
    public ResponseEntity<Map<String, Object>> getBookById(@PathVariable long id) {
        if (id < 1) {
            return ResponseEntity
                    .status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("detail", "Invalid ID: Id must be greater than 0"));
        }
        Optional<Book> optionalBook = books.stream()
                .filter(book -> book.getId() == id)
                .findFirst();

        return optionalBook.<ResponseEntity<Map<String, Object>>>map(book -> ResponseEntity
                .status(HttpStatus.OK)
                .body(Map.of("book", new BookRequest(book.getTitle(), book.getAuthor(), book.getCategory(), book.getRating()))))
                .orElseThrow(() -> new BookNotFoundException(String.format("Book with id %d not found", id)));
    }

    @GetMapping("/books")
    public ResponseEntity<Map<String, Object>> getBooks(@RequestParam(required = false) String category,
                                               @RequestParam(required = false) String title,
                                               @RequestParam(required = false) String author) {
        List<Book> filteredBooks = books.stream()
                .filter(book -> category == null || book.getCategory().equalsIgnoreCase(category))
                .filter(book -> title == null || book.getTitle().equalsIgnoreCase(title))
                .filter(book -> author == null || book.getAuthor().equalsIgnoreCase(author))
                .toList();

        if (filteredBooks.isEmpty()) {
            throw new BookNotFoundException("No books found");
        }
        return ResponseEntity
                .status(HttpStatus.OK)
                .body(Map.of("books", filteredBooks)); // 200 OK
    }

    @PostMapping("/books")
    public  ResponseEntity<Map<String, Object>> createBook(@Valid @RequestBody BookRequest bookRequest){
        boolean isBookExists = books.stream()
                .anyMatch(book ->
                        book.getTitle().equalsIgnoreCase(bookRequest.getTitle()) &&
                        book.getAuthor().equalsIgnoreCase(bookRequest.getAuthor()) &&
                        book.getCategory().equalsIgnoreCase(bookRequest.getCategory()));
        if (isBookExists) {
            throw new BookAlreadyExistsException("Book already exists");
        }
        Book createdBook = createBookFromRequest(bookRequest);
        books.add(createdBook);
        Map<String, Object> responseBody = new HashMap<>();
        responseBody.put("message", "Book created successfully");
        responseBody.put("book", createdBook);
        return ResponseEntity
                .status(HttpStatus.CREATED)    // 201 Created
                .body(responseBody);
    }

    @PutMapping("/books")
    public ResponseEntity<Map<String, Object>> updateBook(@RequestParam String title, @Valid @RequestBody BookRequest updatedBook){
        List<Book> list = books.stream().filter(book -> book.getTitle().equalsIgnoreCase(title))
                .toList();
        if (list.isEmpty()) {
            return ResponseEntity
                    .status(HttpStatus.NOT_FOUND) // 404 Not Found
                    .body(Map.of("detail", String.format("Book(s) with title '%s' not found", title)));
        }
        else if (list.size() > 1) {
            Map<String, Object> responseBody = new HashMap<>();
            responseBody.put("detail", "Multiple books found");
            responseBody.put("books", list);
            return ResponseEntity
                    .status(HttpStatus.CONFLICT) // 409 Conflict
                    .body(responseBody);
        }
        else {
            books.stream()
                    .filter(book -> book.getTitle().equalsIgnoreCase(title))
                    .findFirst()
                    .ifPresent(book -> {
                        book.setTitle(updatedBook.getTitle());
                        book.setAuthor(updatedBook.getAuthor());
                        book.setCategory(updatedBook.getCategory());
                        book.setRating(updatedBook.getRating());
                    });
            return ResponseEntity
                    .status(HttpStatus.OK) // 200 OK
                    .body(Map.of("message", "Book updated successfully"));
        }
    }

    @PutMapping("/books/{id}")
    public ResponseEntity<Map<String, Object>> updateBookById(@PathVariable long id, @RequestBody BookRequest bookRequest){
        if (id < 1) {
            return ResponseEntity
                    .status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("detail", "Invalid ID: Id must be greater than 0"));
        }
        return books.stream()
                .filter(book -> book.getId() == id)
                .findFirst()
                .map(book -> {
                    // Snapshot old values before update
                    Map<String, Object> oldBook = Map.of(
                            "id", book.getId(),
                            "title", book.getTitle(),
                            "author", book.getAuthor(),
                            "category", book.getCategory(),
                            "rating", book.getRating()
                    );

                    // Apply updates
                    book.setTitle(bookRequest.getTitle());
                    book.setAuthor(bookRequest.getAuthor());
                    book.setCategory(bookRequest.getCategory());
                    book.setRating(bookRequest.getRating());

                    // Build response
                    return ResponseEntity.ok(Map.of(
                            "message", "Book updated successfully",
                            "OldBook", oldBook,
                            "UpdatedBook", book
                    ));
                })
                .orElseThrow(() -> new BookNotFoundException(String.format("Book with id: '%d' not found", id)));
    }

    @DeleteMapping(value= "/books")
    public ResponseEntity<Map<String, String>> deleteBookByTitle(@RequestParam String title){

        long before = books.size();
        books.removeIf(book -> book.getTitle().equalsIgnoreCase(title));
        long deleted = before - books.size();

        if (deleted == 0) {
            throw new BookNotFoundException(String.format("Book(s) with title '%s' not found", title));
        }
        String message = deleted == 1
                ? String.format("1 book with title '%s' deleted successfully", title)
                : String.format("%d books with title '%s' deleted successfully", deleted, title);

        return ResponseEntity.ok(Map.of("detail", message));
    }

    @DeleteMapping("/books/{id}")
    public ResponseEntity<Map<String, String>> deleteBookById(@PathVariable long id){
        if (id < 1) {
            return ResponseEntity
                    .status(HttpStatus.BAD_REQUEST)
                    .body(Map.of("detail", "Invalid ID: Id must be greater than 0"));
        }
        boolean bookRemoved = books.removeIf(book -> book.getId() == id);
        if (!bookRemoved) {
            throw new BookNotFoundException(String.format("Book with id: '%s' not found", id));
        }
        return ResponseEntity
                .status(HttpStatus.OK) // 200 OK
                .body(Map.of("message", String.format("Book with id: '%s' deleted successfully", id)));
    }


    private Book createBookFromRequest(BookRequest bookRequest){
        return new Book(
                books.size() + 1L,
                bookRequest.getTitle(),
                bookRequest.getAuthor(),
                bookRequest.getCategory(),
                bookRequest.getRating()
        );
    }
}


