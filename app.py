import streamlit as st
import json

# Load meal data from JSON file
@st.cache_data
def load_meal_data():
    try:
        with open("liondine_meals.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: The file 'liondine_meals.json' was not found.")
        return None

meal_data = load_meal_data()

# Streamlit UI for Home Page
st.title("🍽 Columbia Dining Menu")
st.write("View today's dining options across Columbia's dining halls!")

# Select Meal Time (breakfast, lunch, dinner)
meal_time = st.selectbox("Select a meal time:", ["breakfast", "lunch", "dinner"])

# Display meals for the selected time
if meal_data:
    if meal_time in meal_data:
        for dining_hall, hall_info in meal_data[meal_time].items():
            st.subheader(f"🏛 {dining_hall}")
            st.write(f"⏰ Hours: {hall_info['hours']}")
            
            for category, items in hall_info["menu"].items():
                with st.expander(f"🍽 {category}"):
                    for item in items:
                        st.write(f"- {item}")

    else:
        st.error(f"No data available for {meal_time}. Try again later.")
else:
    st.error("Meal data is unavailable. Please check back later.")

# Navigation to Meal Recommender Page
st.markdown("[👉 Get a Personalized Meal Recommendation](pages/recommender.py)")
