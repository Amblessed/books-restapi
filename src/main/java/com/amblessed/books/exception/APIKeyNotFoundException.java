package com.amblessed.books.exception;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 07-Sep-25
 */


public class APIKeyNotFoundException extends RuntimeException {

    public APIKeyNotFoundException(String message) {
        super(message);
    }
}
