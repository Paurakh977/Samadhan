import subprocess
import os
import random
import json

categories = ["Social Networking", "Entertainment", "Productivity", "Others"]

my_dict = {
    "Facebook": [random.randint(10, 20), random.randint(200, 500)],
    "Instagram": [random.randint(10, 20), random.randint(200, 500)],
    "Setopati": [random.randint(10, 20), random.randint(500, 1000)],
    "Blue Stacks": [random.randint(10, 20), random.randint(700, 900)],
    "Visual Studio Code": [random.randint(15, 20), random.randint(1000, 1200)],
    "Qt designer": [random.randint(15, 20), random.randint(800, 1000)],
    "Adobe PhotoShop": [random.randint(15, 20), random.randint(100, 500)],
    "Word": [random.randint(15, 20), random.randint(50, 200)],
    "Spotify": [random.randint(10, 20), random.randint(300, 600)],
    "WhatsApp": [random.randint(10, 20), random.randint(100, 300)],
    "Telegram": [random.randint(10, 20), random.randint(50, 300)],
    "Netflix": [random.randint(10, 20), random.randint(500, 800)],
    "Slack": [random.randint(15, 20), random.randint(300, 600)],
    "Zoom": [random.randint(15, 20), random.randint(100, 400)],
    "Trello": [random.randint(10, 20), random.randint(50, 200)],
    "Google Chrome": [random.randint(20, 25), random.randint(1200, 1500)],
    "Adobe Illustrator": [random.randint(15, 20), random.randint(200, 500)],
    "Evernote": [random.randint(10, 20), random.randint(50, 150)],
    "LinkedIn": [random.randint(10, 20), random.randint(100, 300)],
    "TikTok": [random.randint(10, 20), random.randint(200, 400)],
    "Discord": [random.randint(10, 20), random.randint(300, 500)],
    "Skype": [random.randint(10, 20), random.randint(150, 350)],
    "Microsoft Excel": [random.randint(15, 20), random.randint(200, 600)],
    "Google Meet": [random.randint(10, 20), random.randint(100, 300)],
    "Snapchat": [random.randint(10, 20), random.randint(150, 400)],
    "Amazon": [random.randint(20, 25), random.randint(500, 1000)],
    "Spotify": [random.randint(10, 20), random.randint(300, 600)],
    "Notion": [random.randint(10, 20), random.randint(50, 200)],
}


current_directory = os.path.dirname(os.path.abspath(__file__))
sh_script = os.path.join(current_directory, "parsher.sh")


formatted_input = f"Hey gemini, here are the categories {categories} and these are some of the names of the applications {list(my_dict.keys())}. Categorize which application falls under which category yourself. Please do not put any apps in 'Others' if they can be categorized elsewhere. I want you to return a dictionary where keys are the categories and the values are the list of the apps for each category. JUST GIVE ME THE DICT IN RESPONSE NO OTHER INFORMATION OR TEXT"

result = subprocess.run(
    ["bash", sh_script, formatted_input], stdout=subprocess.PIPE, text=True
)

data = result.stdout.strip()

parsed_data = json.loads(data)

text_value = parsed_data["candidates"][0]["content"]["parts"][0]["text"]

cleaned_text = (
    text_value.replace("app_categories =", "")
    .replace("json", "")
    .replace("```python", "")
    .replace("```", "")
    .replace("print(app_categories)", "")
    .strip()
)

cleaned_text = cleaned_text.replace("'", '"')
try:
    my_dict = json.loads(cleaned_text)
    print(type(my_dict))  # Should print <class 'dict'>
    print(my_dict)  # Prints the dictionary
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
