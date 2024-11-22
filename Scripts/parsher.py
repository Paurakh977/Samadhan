import subprocess
import os
import random
import json


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


def filtering_data(
    raw_prompt_dict: dict[str : list[int:float]],
    categorized_prompt_dict: dict[str : list[str]],
):
    data = {
        "Social Networking": {hour: 0 for hour in range(24)},
        "Entertainment": {hour: 0 for hour in range(24)},
        "Productivity": {hour: 0 for hour in range(24)},
        "Others": {hour: 0 for hour in range(24)},
    }

    seconds_to_minutes = lambda seconds: round(seconds / 60, 2)
    raw_prompt_dict = {
        k: [v[0], seconds_to_minutes(v[1])] for k, v in raw_prompt_dict.items()
    }
    
    for app, (hour, minutes) in raw_prompt_dict.items():
    # Find which category the app belongs to in 'a'
        for category, app_list in categorized_prompt_dict.items():
            if app in app_list:
                data[category][hour] += minutes
                
    return data


def categorize_app(
    input_prompt_dict,
    categories=["Social Networking", "Entertainment", "Productivity", "Others"],
):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    sh_script = os.path.join(current_directory, "parsher.sh")

    formatted_input = f"Hey gemini, here are the categories {categories} and these are some of the names of the applications {list(input_prompt_dict.keys())}. Categorize which application falls under which category yourself. Please do not put any apps in 'Others' if they can be categorized elsewhere. I want you to return a dictionary where keys are the categories and the values are the list of the apps for each category. JUST GIVE ME THE DICT IN RESPONSE NO OTHER INFORMATION OR TEXT"

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
        return filtering_data(input_prompt_dict, my_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
