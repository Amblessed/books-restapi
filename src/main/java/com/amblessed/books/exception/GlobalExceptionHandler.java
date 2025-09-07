package com.amblessed.books.exception;

/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 07-Sep-25
 */

import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import org.springframework.context.support.DefaultMessageSourceResolvable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.net.URI;
import java.sql.SQLIntegrityConstraintViolationException;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {


    @ExceptionHandler({ConstraintViolationException.class, MethodArgumentNotValidException.class, SQLIntegrityConstraintViolationException.class})
    public ProblemDetail handleException(Exception exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("timestamp", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.BAD_REQUEST.getReasonPhrase());
        problemDetail.setInstance(problemDetail.getInstance());
        problemDetail.setProperties(map);
        String detailMessage;

        switch (exception) {
            case MethodArgumentNotValidException ex ->
                // Collect all default messages from field errors
                detailMessage = ex.getBindingResult()
                        .getFieldErrors()
                        .stream()
                        .map(DefaultMessageSourceResolvable::getDefaultMessage)
                        .reduce((a, b) -> a + "; " + b)
                        .orElse("Validation failed");
            case ConstraintViolationException ex ->
                // Collect violation messages
                detailMessage = ex.getConstraintViolations()
                        .stream()
                        .map(ConstraintViolation::getMessage)
                        .reduce((a, b) -> a + "; " + b)
                        .orElse("Validation failed");
            default -> detailMessage = exception.getMessage();
        }
        problemDetail.setDetail(detailMessage);
        return problemDetail;
    }

    @ExceptionHandler({BookAlreadyExistsException.class})
    public ProblemDetail handleAlreadyExistException(Exception exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("timestamp", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.CONFLICT);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.CONFLICT.getReasonPhrase());
        problemDetail.setDetail(exception.getMessage());
        problemDetail.setProperties(map);
        problemDetail.setInstance(problemDetail.getInstance());
        return problemDetail;
    }


    @ExceptionHandler(BookNotFoundException.class)
    public ProblemDetail handleBookNotFoundException(BookNotFoundException exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("timestamp", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.NOT_FOUND.getReasonPhrase());
        problemDetail.setDetail(exception.getMessage());
        problemDetail.setProperties(map);
        return problemDetail;
    }

}
