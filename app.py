import streamlit as st
import json
import random

# Load meal data from JSON file
@st.cache_data
def load_meal_data():
    with open("liondine_meals.json", "r") as file:
        return json.load(file)

meal_data = load_meal_data()

# Streamlit UI
st.title("Columbia Dining Meal Recommender")
st.write("Find meal options available based on your dining preferences!")

# User Inputs
meal_time = st.selectbox("Select Meal Time", ["breakfast", "lunch", "dinner"])
dining_hall = st.selectbox("Select Dining Hall", list(meal_data[meal_time].keys()))
user_goal = st.selectbox("Select Weight Goal", ["lose weight", "gain weight", "maintain"])
exercise_amt = st.text_input("How much exercise do you do weekly in hours?", 0)

# Function to recommend meal
def recommend_meal(meal_time, dining_hall):
    hall_data = meal_data.get(meal_time, {}).get(dining_hall, {})
    if hall_data and "menu" in hall_data:
        categories = list(hall_data["menu"].keys())
        selected_category = st.selectbox("Select a Food Category", categories)
        meals = hall_data["menu"].get(selected_category, [])
        return random.choice(meals) if meals else "No meals available."
    return "Dining hall is closed or no data available."

if st.button("Get Meal Recommendation"):
    meal = recommend_meal(meal_time, dining_hall)
    st.subheader("Recommended Meal")
    st.write(f"**Meal:** {meal}")
