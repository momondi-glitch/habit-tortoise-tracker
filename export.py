import csv
import json
import os

def export_habits_to_csv():
    if not os.path.exists("habits.json"):
        print("😢 No data to export.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

    if not habits:
        print("😢 No habits to export.")
        return
    
    with open("habits_export.csv", "w", newline="") as csvfile:
        fieldnames = ["Name", "Per Day", "Per Week", "Importance", "Streak", "Total Completions", "Reminders"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for habit in habits:
            default_reminders = ", ".join(habit.get("reminders", {}).get("default", []))
            custom_reminders = habit.get("reminders", {}).get("custom", {})
            custom_summary = "; ".join([f"{day}: {', '.join(times)}" for day, times in custom_reminders.items()])
            reminder_summary = f"Default: {default_reminders} | Custom: {custom_summary}"

            writer.writerow({
                "Name": habit["name"],
                "Per Day": habit["goal_per_day"],
                "Per Week": habit["goal_per_week"],
                "Importance": habit["importance"],
                "Streak": habit["streak"],
                "Total Completions": len(habit.get("completions", [])),
                "Reminders": reminder_summary
            })

    print("✅ Habit data exported to 'habits_export.csv'")

def export_habits_to_html():
    if not os.path.exists("habits.json"):
        print("😢 No data to export.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

    if not habits:
        print("😢 No habits to export.")
        return
    
    html_content = """
    <html>
    <head>
        <title> Toto's Habit Tracker Export</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; padding: 30px; background-color: #f8f9fa; color: #333; }
            h1 { color: #2d6a4f; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
            th { background-color: #95d5b2; color: #1b4332; }
            td { background-color: #ffffff; }
            .footer { margin-top: 40px; font-size: 0.9em; color: #777; text-align: center; }
            .logo { font-size: 3em; text-align: center; }
        
        </style>
    </head>
    <body>
        <h1>🐢 Toto's Habit Tracker - Export</h1>
        <table>
            <tr>
                <th>Name</th>
                <th>Per Day</th>
                <th>Per Week</th>
                <th>Importance</th>
                <th>Streak</th>
                <th>Total Completions</th>
                <th>Reminders</th>
            </tr>
    """

    for habit in habits:
         default_reminders = ", ".join(habit.get("reminders", {}).get("default", []))
         custom_reminders = habit.get("reminders", {}).get("custom", {})
         custom_summary = "; ".join([f"{day}: {', '.join(times)}" for day, times in custom_reminders.items()])
         reminder_summary = f"Default: {default_reminders} | Custom: {custom_summary}"

         html_content += f"""
            <tr>
                <td>{habit['name']}</td>
                <td>{habit['goal_per_day']}</td>
                <td>{habit['goal_per_week']}</td>
                <td>{habit['importance']}</td>
                <td>{habit['streak']}</td>
                <td>{len(habit.get('completions', []))}</td>
                <td>{reminder_summary}</td>
            </tr>
        """

    html_content += """
        </table>
        <div class="footer">
            Toto the Tortoise generated this 💚 - One habit at a time 🌱
        </div>

    </body>
    </html>
    """

    with open("habits_export.html", "w") as file:
        file.write(html_content)

    print("✅ Habit data exported to 'habits_export.html'")
