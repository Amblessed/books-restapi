package com.amblessed.books.entity;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 06-Sep-25
 */

import jakarta.validation.constraints.Min;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Book {

    @Min(value = 1, message = "Id must be greater than 0")
    private long id;
    private String title;
    private String author;
    private String category;


    private int rating;
}
