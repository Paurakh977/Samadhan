#!/bin/bash

# Define your API key (ensure it's valid)
API_KEY="AIzaSyD45DzCPVEza4VlQK-i_E8nL_NKUkJgfTA"

# Accept the user input (text passed from Python)
USER_INPUT=$1

# Check if USER_INPUT is empty
if [ -z "$USER_INPUT" ]; then
  echo "Error: No input provided."
  exit 1
fi

# Make the curl request to the Gemini API
response=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [
      {
        \"role\": \"user\",
        \"parts\": [
          {
            \"text\": \"${USER_INPUT}\"
          }
        ]
      }
    ],
    \"generationConfig\": {
      \"temperature\": 0.9,
      \"topK\": 40,
      \"topP\": 0.95,
      \"maxOutputTokens\": 8192,
      \"responseMimeType\": \"text/plain\"
    }
  }")

# Check if the curl request succeeded
if [ $? -ne 0 ]; then
  echo "Error: Curl request failed."
  exit 1
fi

# Output the response as is (without any filtering)
echo "$response" 