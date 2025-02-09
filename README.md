# DevFestLionDiet

LionDiet is a website intended to help Columbia students with access to a mealplan decide what their next meal should be based on their nutritional goals. They will provide the site with their age, weight, height, weekly exercise amount, and intended health goal. LionDiet will reccommend an available Dining Hall and meal.

LionDiet operates by scraping LionDine, a daily calendar and menu of all available meals at the Columbia Dining Halls. It will then call groq.api to obtain the nutritional value of all the meals. Here are the nutritional facts assessed by groq:
- Protein
- Carbohydrates
- Fats
- Fiber
- Sugars
- Sodium
- Saturated vs. unsaturated fats
- Micronutrients

LionDiet will take the user's input and use groq to assess the nutritonal goals of the user, how much protein should they consume? How much carbohydrates? And so forth. After having considered the optimal diet for the user, LionDiet will use groq to compare the needs of the user with the availble meals in the Dining Halls and give back a reccommended meal, or meal plan for the day.


**Run app in main folder**
   ```bash
   streamlit run app.py
   ```


