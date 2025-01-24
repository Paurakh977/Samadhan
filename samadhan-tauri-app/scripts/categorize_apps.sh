#!/bin/bash

API_KEY="AIzaSyD45DzCPVEza4VlQK-i_E8nL_NKUkJgfTA"

# Accept JSON object of app names and their usage times
APP_BATCH=$1

if [ -z "$APP_BATCH" ]; then
  echo "Error: No input provided."
  exit 1
fi

# Craft a more specific prompt for app categorization with usage times
PROMPT="Given this JSON object of applications and their usage times in seconds: ${APP_BATCH}
Analyze each application and categorize it, then sum the times for apps in the same category.
Return ONLY a JSON object where:
- Keys are categories: ['Productivity', 'Entertainment', 'Social Networking', 'Other']
- Values are the total seconds spent in each category
Example input: {'VS code': 300, 'instagram': 120}
Example output: {'Productivity': 300, 'Social Networking': 120}
Rules:
'"

response=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [
      {
        \"role\": \"user\",
        \"parts\": [
          {
            \"text\": \"${PROMPT}\"
          }
        ]
      }
    ],
    \"generationConfig\": {
      \"temperature\": 0.1,
      \"topK\": 1,
      \"topP\": 0.1,
      \"maxOutputTokens\": 1024
    }
  }")

echo "$response" 