package com.amblessed.books.exception;

/*
 * @Project Name: university-management-system
 * @Author: Okechukwu Bright Onwumere
 * @Created: 09-Sep-24
 */

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.net.URI;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {


    //@ExceptionHandler({ConstraintViolationException.class, MethodArgumentNotValidException.class, SQLIntegrityConstraintViolationException.class, EmptyFileException.class})
    public ProblemDetail handleConstraintViolationException(Exception exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("date", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.BAD_REQUEST.getReasonPhrase());
        problemDetail.setDetail(exception.getMessage());
        problemDetail.setInstance(problemDetail.getInstance());
        problemDetail.setProperties(map);
        return problemDetail;
    }

    //@ExceptionHandler({FileExistsException.class, AlreadyExistsException.class})
    public ProblemDetail handleAlreadyExistException(Exception exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("date", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.CONFLICT);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.CONFLICT.getReasonPhrase());
        problemDetail.setDetail(exception.getMessage());
        problemDetail.setInstance(problemDetail.getInstance());
        problemDetail.setProperties(map);
        return problemDetail;
    }


    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleFacultyNotFoundException(ResourceNotFoundException exception) {
        Map<String, Object> map = new HashMap<>();
        map.put("date", LocalDateTime.now().toString());
        ProblemDetail problemDetail = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        problemDetail.setType(URI.create("http://localhost:8080/api/v1/common-errors"));
        problemDetail.setTitle(HttpStatus.NOT_FOUND.getReasonPhrase());
        problemDetail.setDetail(exception.getMessage());
        problemDetail.setInstance(problemDetail.getInstance());
        problemDetail.setProperties(map);
        return problemDetail;
    }

}
