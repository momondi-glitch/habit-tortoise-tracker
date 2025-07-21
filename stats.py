import calendar
from datetime import datetime
import json
import os


def view_streak_history():
    if not os.path.exists("habits.json"):
        print(" No habits to show streaks for.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

    if not habits:
        print ("No habits found.")
        return
    
    print("\n📈 Streak History:")
    total_streak = 0
    max_streak = 0
    top_habit = ""

    for habit in habits:
        streak = habit["streak"]
        total_streak += streak
        if streak > max_streak:
            max_streak = streak
            top_habit = habit["name"]

        print(f"🔹 {habit['name']}: {streak} ")
    
    print("\n🥇 Top streak:")
    if max_streak > 0:
        print(f"👉 {top_habit} with {max_streak} days in a row!")
    else:
        print("No streaks yet. Let's build some together 🐢...")

    print(f"\n🔥 Tota; streak points across all habits: {total_streak}")   

def view_calendar():
    if not os.path.exists("habits.json"):
        print("😢 No habits to show calendar for.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

    if not habits:
        print("😢 No habits available.")
        return

    print("\n📅 Select a habit to view its calendar:")
    for idx, habit in enumerate(habits, 1):
        print(f"{idx}. {habit['name']}")

    choice = input("Enter number: ")
    if not choice.isdigit() or int(choice) not in range(1, len(habits) + 1):
        print("❌ Invalid selection.")
        return

    habit = habits[int(choice) - 1]
    completed_dates = set(habit["completions"])

    # Get current month
    now = datetime.now()
    year, month = now.year, now.month
    cal = calendar.monthcalendar(year, month)

    print(f"\n🗓️ {calendar.month_name[month]} {year} – {habit['name']} Completions")
    print("Mo Tu We Th Fr Sa Su")

    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                mark = "✅" if date_str in completed_dates else " . "
                line += mark + " "
        print(line)