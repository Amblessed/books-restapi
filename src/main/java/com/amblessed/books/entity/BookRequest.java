package com.amblessed.books.entity;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 06-Sep-25
 */

import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.validator.constraints.Range;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class BookRequest {

    @NotEmpty(message = "Title is required")
    @Size(min = 10, max = 50, message = "Title must be between 10 and 50 characters")
    private String title;

    @NotEmpty(message = "Author is required")
    @Size(min = 10, max = 25, message = "Author must be between 10 and 25 characters")
    private String author;

    @NotEmpty(message = "Category is required")
    @Size(min = 5, max = 20, message = "Category must be between 5 and 20 characters")
    private String category;

    @Range(min = 1, max = 5, message = "Invalid rating: Rating must be between 1 and 5")
    private int rating;
}
