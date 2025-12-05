🥗 AI Nutrition Assistant
Personalized 7-Day Meal Plan Generator + Daily Nutrition & Exercise Tracking

The AI Nutrition Assistant is a Gen-AI powered system that creates a personalized 7-day meal plan based on user details (age, height, weight, goals, activity level, dietary preference) and tracks daily calorie intake vs calories burned using an integrated nutrition–exercise database.

📌 Features
✅ 1. Personalized 7-Day Meal Plan (AI-Generated)

The system collects user details:

Age

Gender

Height, Weight

Dietary preference (Veg / Non-Veg / Vegan)

Fitness goal (Weight Loss / Gain / Maintenance)

Activity level

Then it generates:

Daily meals (Breakfast, Lunch, Dinner, Snacks)

Calories per meal

Macro breakdown: Protein, Carbs, Fats

A complete 7-day meal plan report

✅ 2. Nutrition Intake Tracking

Users can log foods they ate:

Food name

Quantity

Meal type

Timestamp

The system stores:

Total calories

Carbs

Protein

Fat

✅ 3. Exercise Tracking

Users can record:

Exercise type

Duration

Calories burned

Stored daily in the database.

✅ 4. Daily Summary (Automated)

Every day, the system automatically calculates:

“Yesterday you consumed X calories and burned Y calories, resulting in a net balance of Z.”

✅ 5. Database Integration

A structured database stores:

User profile

Meal plan history

Food intake logs

Exercise logs

Daily summaries

Supports SQLite / PostgreSQL.

🧠 Tech Stack
Component	Technology
Backend	Python
AI Model	OpenAI (Meal Plan Generation)
Database	SQLite / PostgreSQL
Frameworks	Flask / FastAPI (optional)
Tools	Pandas, NumPy
🚀 How It Works
1️⃣ User Inputs

User fills a form or API body with personal details.

2️⃣ AI Meal Plan Generation

A Gen-AI model processes the data and generates a 7-day meal plan with macros.

3️⃣ Data Storage

Nutrition + exercise logs are saved daily.

4️⃣ Daily Summary Engine

A scheduled script computes:

Total calories eaten

Total calories burned

Net daily calories

5️⃣ User Dashboard / API

Displays meal plan + daily summary.

📂 Project Structure
ai-nutrition/
│── model/
│   ├── meal_plan_generator.py
│   ├── nutrition_analysis.py
│── database/
│   ├── schema.sql
│   ├── db.py
│── app/
│   ├── routes.py
│   ├── utils.py
│── reports/
│── README.md
│── requirements.txt
│── main.py

🛠️ Installation
git clone https://github.com/<your-username>/ai-nutrition.git
cd ai-nutrition
pip install -r requirements.txt

🧪 Usage
Generate Meal Plan
python main.py --generate-meal-plan

Log Food
python main.py --log-food

Log Exercise
python main.py --log-exercise

Get Daily Summary
python main.py --daily-summary

📈 Future Enhancements

Add mobile app UI

Auto-sync with fitness trackers

Voice-based input (Proton Assistant integration)

PDF report export for meal pl
