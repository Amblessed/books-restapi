package com.amblessed.books.exception;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 07-Sep-25
 */


public class RequestFailedException extends RuntimeException {

    public RequestFailedException(String message) {
        super(message);
    }
}
