from datetime import date 

def send_reminders(habit):
    today = date.today().isoformat()
    reminders = []

    for habit in habit: 
        if today not in habit.get("completions", []):
            reminders.append(f"🔔 Reminder: You haven't completed '{habit['name']}' today!")
    return reminders

    