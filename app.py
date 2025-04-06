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
        # Use columns for better layout
        st.subheader(f"Menu for {meal_time.capitalize()}")

        for dining_hall, hall_info in meal_data[meal_time].items():
            st.markdown(f"## 🏛 {dining_hall}")
            st.write(f"⏰ **Hours:** {hall_info['hours']}")

            # Create a grid-like station display
            st.markdown("### Available Stations & Menu:")
            cols = st.columns(3)  # Adjust columns based on number of stations

            stations = list(hall_info["menu"].items())  # Convert dictionary to list for indexing

            for index, (station_name, items) in enumerate(stations):
                with cols[index % 3]:  # Distribute across columns
                    st.markdown(f"**{station_name}**")
                    for item in items:
                        st.write(f"- {item}")

            st.markdown("---")  # Divider for different dining halls

    else:
        st.error(f"No data available for {meal_time}. Try again later.")
else:
    st.error("Meal data is unavailable. Please check back later.")

# Navigation to Meal Recommender Page
if st.button("🔮 Get a Meal Recommendation"):
    st.switch_page("pages/recommender.py")