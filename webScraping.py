import requests
from bs4 import BeautifulSoup
import json


# Read standardized_dishes.json file and convert the data into a dictionary stored in the variable standardized_data
import os
# Load standardized dishes from JSON if available
standardized_file = "standardized_dishes.json"
if os.path.exists(standardized_file):
    with open(standardized_file, "r", encoding="utf-8") as std_file:
        standardized_data = json.load(std_file)
else:
    standardized_data = {}


# Base URL for Lion Dine meals
meal_types = ["breakfast", "lunch", "dinner"]
base_url = "https://liondine.com/"

# Dictionary to store meal data
liondine_data = {}

# Headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


for meal in meal_types:
    url = f"{base_url}{meal}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser") # removed .text from response


        meal_data = {}  # Store data per meal type

        # Find all dining locations
        dining_sections = soup.find_all("div", class_="col")

        for section in dining_sections:
            dining_location = section.find("h3").text.strip()
            hours = section.find("div", class_="hours").text.strip() if section.find("div", class_="hours") else "Unknown Hours"
            menu_items = {}

            # Find all menu categories
            menu_categories = section.find_all("div", class_="food-type")
            for category in menu_categories:
              category_name = category.text.strip()  # Get category name directly
              # Find all food items following the category
              items = []
              for sibling in category.find_next_siblings():
                if sibling.name == "div" and "food-name" in sibling.get("class", []):
                    items.append(sibling.text.strip())
                else:
                    # Stop when we encounter another category or non-food item
                    break
                      
                if items:
                    menu_items[category_name] = items

            # Store data under venue name
            meal_data[dining_location] = {
                "hours": hours,
                "menu": menu_items
            }

        # Store under meal type (breakfast, lunch, dinner)
        liondine_data[meal] = meal_data

    else:
        print(f"Failed to fetch {meal} page. Status code: {response.status_code}")

# Save everything into a JSON file
with open("liondine_meals.json", "w", encoding="utf-8") as json_file:
    json.dump(liondine_data, json_file, indent=4, ensure_ascii=False)

print("Scraping complete! Data saved to liondine_meals.json")
