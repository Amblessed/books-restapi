package com.amblessed.books.service;



/*
 * @Project Name: books
 * @Author: Okechukwu Bright Onwumere
 * @Created: 08-Sep-25
 */

import com.amblessed.books.exception.APIKeyNotFoundException;
import com.amblessed.books.exception.ErrorResponseException;
import com.amblessed.books.exception.RequestFailedException;
import okhttp3.*;
import org.springframework.stereotype.Service;
import org.json.*;


import java.util.Arrays;
import java.util.List;

@Service
public class OpenAIService {

    OkHttpClient client = new OkHttpClient();

    public List<String> getRecommendations(String prompt)  {
        String apiKey = System.getenv("OPENAI_API_KEY");
        if (apiKey != null)
        {
            System.out.println("API Key loaded successfully!");
        }
        else {
            throw new APIKeyNotFoundException("API Key not found in environment variables.");
        }
        
        // Create JSON body
        JSONObject jsonBody = new JSONObject();
        jsonBody.put("model", "gpt-4");
        jsonBody.put("messages", new JSONObject[]
                {
                new JSONObject()
                        .put("role", "user")
                        .put("content", "List the book titles only, one per line, without any numbering or additional text. " + prompt)
        });
        jsonBody.put("max_tokens", 1500);
        jsonBody.put("temperature", 0.7);

        // Create request
        RequestBody body = RequestBody.create(jsonBody.toString(), MediaType.parse("application/json"));
        Request request = new Request.Builder()
                .url("https://api.openai.com/v1/chat/completions")
                .addHeader("Content-Type", "application/json")
                .addHeader("Authorization", "Bearer " + apiKey)
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String responseBody = response.body().string();
                System.out.println(responseBody);
                JSONObject jsonResponse = new JSONObject(responseBody);
                String reply = jsonResponse
                        .getJSONArray("choices")
                        .getJSONObject(0)
                        .getJSONObject("message")
                        .getString("content");
                
                // Split the response by newlines
                return Arrays.stream(reply.split("\\n"))
                        .map(String::trim)
                        .filter(line -> !line.isEmpty())
                        .toList();
            } else {
                throw new RequestFailedException("Request failed: " + response.code() + " " + response.message());
            }
        } catch (Exception e)
        {
            throw new ErrorResponseException("Error processing response: " + e.getMessage());
        }
    }
}
