import streamlit as st
import json
import requests
import os
import random
from groq import Groq

# Load meal data from JSON file
@st.cache_data
def load_meal_data():
    try:
        with open("liondine_meals.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: The file 'liondine_meals.json' was not found in the repository.")
        return None

meal_data = load_meal_data()

print(meal_data)

# Streamlit UI
st.title("Columbia Dining Meal Recommender")
st.write("Find meal options available based on your dining preferences!")

# User Inputs
user_age = st.number_input("What is your age?", min_value=0, step=1)
user_weight_lbs = st.number_input("What is your weight in pounds?", min_value=0, step=1)
user_height_inches = st.number_input("What is your height in inches?", min_value=0, step=1)
meal_time = st.selectbox("Select Meal Time", ["breakfast", "lunch", "dinner"])
user_goal = st.selectbox("Select Weight Goal", ["lose weight", "gain weight", "maintain"])
user_exercise_hours = st.number_input("How many hours do you exercise per week?", min_value=0, step=1)

# Convert user inputs to metric system
user_weight_kg = round(user_weight_lbs * 0.453592, 2)
user_height_cm = round(user_height_inches * 2.54, 2)

# Map exercise hours to activity level
if user_exercise_hours == 0:
    user_exercise_level = "Sedentary"
elif user_exercise_hours <= 3:
    user_exercise_level = "Light Activity"
elif user_exercise_hours <= 6:
    user_exercise_level = "Moderate Activity"
elif user_exercise_hours <= 10:
    user_exercise_level = "Very Active"
else:
    user_exercise_level = "Extremely Active"

# Retrieve API Key from environment variable
GROQ_API_KEY = os.getenv("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")
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Function to call Groq's API
def chat_with_groq(system_prompt, user_prompt):

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
    )

    # url = "https://api.groq.com/v1/chat/completions"

    # headers = {
    #     "Authorization": f"Bearer {GROQ_API_KEY}",
    #     "Content-Type": "application/json"
    # }

    # data = {
    #     "model": "llama3-8b-8192",
    #     "messages": [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     "temperature": 0.7
    # }

    # response = requests.post(url, headers=headers, json=data)

    # print(response)
    if response:
        return response.choices[0].message.content
    else:
        st.error(f"Groq API Error: {response.status_code}, {response.text}")
        return None

# Step 1: Determine Nutritional Needs
def get_nutritional_needs(user_age, user_weight_kg, user_height_cm, user_exercise_level, user_goal):
    system_prompt = (
        "You are a nutrition assistant helping Columbia University students create a diet plan that aligns with their dining plan. "
        "Your task is to determine the weekly nutrient and calorie requirements based on personal attributes and lifestyle factors. "
        "Ensure that your calculations are dynamic and based on the user's goal (e.g., weight gain, weight loss, maintenance, athletic performance)."
        "This json file {meal_data} has the meals of the day. Please just include that meal in the response (nothing else needed)."

    )

    user_prompt = f"""
    My user needs a personalized diet plan based on their Columbia dining plan. To begin, determine their weekly nutrient and calorie needs.
    Consider the following user details:

    - Age: {user_age}
    - Weight: {user_weight_kg} kg
    - Height: {user_height_cm} cm
    - Exercise Level: {user_exercise_level}
    - Goal: {user_goal}

    Use the Mifflin-St Jeor Equation for BMR, adjust for TDEE, and modify calorie intake based on goal. 
    """

    response = chat_with_groq(system_prompt, user_prompt)
    # return json.loads(response) if response else None
    return response

# Streamlit Button for Meal Recommendation
if st.button("Get Meal Recommendation"):
    st.write("Calculating your nutritional needs...")
    nutritional_needs = get_nutritional_needs(user_age, user_weight_kg, user_height_cm, user_exercise_level, user_goal)

    st.markdown(f"{nutritional_needs}")
    
