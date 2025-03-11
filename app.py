# Note: there are many notes in this file which I need to implement

# I need to change the current meal recommender to a weekly plan that only includes the meals that are available every day
    # Completed: Add new file with standardized meals
    # Completed: write python code for merging new file with scraped data file 
    # Run/Test application so far
    # Add Barnard Dining Halls for standardized data
    # Prompt Engineering to overcome issue of too much data for API

# Create another funcitonality of the app where the user can get one meal recommendations (instead of a weekly plan) 
    # For this function, I need to make sure that the application recommends a meal by reading the website in real time to see the current open locations and menus
    # Somehow link the api to the real time online data of the menus 
    #Somehow make sure that it can also look at the json file to see what general everyday meals are available, to see whethter there are suggestion from there that it can give

# Change Groq api to gemini 

# Consider adding a feature like voice chat: where you converse with the AI (It asks you the input questions, receives answers, processes them and suggest a plan/meal

# Consider making it able to diversify meals (eg from JohnJay 200g salad, 300g noodles with tomato sauce, and a banana)

# Add more options for user input: They should be able to select their dining plan and the api should usggest something based on this restriction.

# Think about this problem: I am creating a weekly plan, but many meals are only published on the day, so the weekly plan will only include standardized meals - perhaps calculate the likelihood of a certain meal being at a certain location (e.g chicken at JohnJay)

import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
from groq import Groq

exec(open("webScraping.py").read())

# Load meal data from JSON file
@st.cache_data
def load_meal_data():
    try:
        with open("liondine_meals.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: The file 'liondine_meals.json' was not found.")
        return None

meal_data = load_meal_data()

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
# Note: Look at this api implementation and compare it to BankAccount.py usage
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to call Groq's API
# Note: Change to Gemini API
def chat_with_groq(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model="mixtral-8x7b-32768",
    )

    return response.choices[0].message.content if response else None

# Step 1: Determine Nutritional Needs & Recommend a Meal
def get_meal_recommendation(user_age, user_weight_kg, user_height_cm, user_exercise_level, user_goal, meal_time):
    system_prompt = f"""
    You are a Columbia University dining assistant. 
    Your task is to recommend a meal based on the user's preferences and available Columbia Dining meals.
    Only return the meal recommendation. No additional text, calculations, or explanations.
    """

    user_prompt = f"""
    My user needs a meal recommendation from Columbia Dining. 
    Consider their details:

    - Age: {user_age}
    - Weight: {user_weight_kg} kg
    - Height: {user_height_cm} cm
    - Exercise Level: {user_exercise_level}
    - Goal: {user_goal}


    Use only the meals listed in this JSON file: {meal_data}.  
    Your response should be in this format:  
    Based on the Columbia dining plan, for {meal_time} I recommend [insert food] from [insert dininghall]
    And explain why this meal is recommended in 1-2 sentences.
    """

    response = chat_with_groq(system_prompt, user_prompt)
    return response

# Streamlit Button for Meal Recommendation
if st.button("Get Meal Recommendation"):
    st.write("Fetching your meal recommendation...")
    meal_recommendation = get_meal_recommendation(user_age, user_weight_kg, user_height_cm, user_exercise_level, user_goal, meal_time)

    if meal_recommendation:
        st.markdown(meal_recommendation)
    else:
        st.error("Failed to retrieve a meal recommendation. Please try again.")
