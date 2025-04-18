# Description: This file contains the Streamlit UI and logic for the Columbia Dining Meal Recommender.
# It uses the Gemini API to generate responses and provide meal recommendations based on user inputs.

import streamlit as st
import json
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

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
user_age = st.text_input("What is your age?", placeholder="Enter your age here")

# Validate input and ensure it's a positive number
if user_age:
    try:
        user_age = float(user_age)
        if user_age <= 0:
            st.error("Please enter a valid age greater than 0.")
    except ValueError:
        st.error("Please enter a numeric value.")
    
user_weight_lbs = st.text_input("What is your weight in pounds?", placeholder="Enter your weight here")
if user_weight_lbs:
    try:
        user_weight_lbs = float(user_weight_lbs)
        if user_weight_lbs <= 0:
            st.error("Please enter a valid weight greater than 0.")
    except ValueError:
        st.error("Please enter a numeric value.")

user_height_inches = st.text_input("What is your height in inches?", placeholder="Enter your height here")
if user_height_inches:
    try:
        user_height_inches = float(user_height_inches)
        if user_height_inches <= 0:
            st.error("Please enter a valid height greater than 0.")
    except ValueError:
        st.error("Please enter a numeric value.")

meal_time = st.selectbox("Select Meal Time", ["breakfast", "lunch", "dinner"])

user_goal = st.selectbox("Select Weight Goal", ["lose weight", "gain weight", "maintain"])

user_exercise_hours = st.text_input("How many hours do you exercise per week?", placeholder="Enter hours here")
# Convert input to float safely
try:
    user_exercise_hours = float(user_exercise_hours) if user_exercise_hours else 0  # Default to 0 if empty
    if user_exercise_hours < 0:
        st.error("Please enter a valid number of hours.")
except ValueError:
    st.error("Please enter a numeric value.")
    user_exercise_hours = 0  # Ensure it's a valid number

# Convert user inputs to metric system
# Note: This isn't actually neccessary, but it's a good practice to convert units for consistency
if user_weight_lbs and user_height_inches:
    try:
        user_weight_kg = round(float(user_weight_lbs) * 0.453592, 2)
        user_height_cm = round(float(user_height_inches) * 2.54, 2)
    except ValueError:
        st.error("Invalid input detected. Please enter numbers only.")
else:
    user_weight_kg = None
    user_height_cm = None

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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Function to call Gemini's API
def chat_with_gemini(system_prompt, user_prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([system_prompt, user_prompt])

    return response.text if response else None

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

    response = chat_with_gemini(system_prompt, user_prompt)
    return response

# Streamlit Button for Meal Recommendation
if st.button("Get Meal Recommendation"):
    st.write("Fetching your meal recommendation...")
    meal_recommendation = get_meal_recommendation(user_age, user_weight_kg, user_height_cm, user_exercise_level, user_goal, meal_time)

    if meal_recommendation:
        st.markdown(meal_recommendation)
    else:
        st.error("Failed to retrieve a meal recommendation. Please try again.")

# Back to Home Page
if st.button("🏠 Back to Menu"):
    st.switch_page("app.py")