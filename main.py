from ast import Import
import json
import os
from habit import Habit
import datetime
import calendar
from datetime import datetime
from utils import get_progress_bar
from stats import view_streak_history, view_calendar
from reminder import send_reminders
from export import export_habits_to_csv, export_habits_to_html
def welcome_screen():
    print("======================================================")
    print("    WELCOME, TOTO THE TORTOISE IS HAPPY TO SEE YOU    ")
    print("======================================================")
    print("Hi there! I'm Toto, your little tortoise buddy.")
    print("I grow healthier every time you complete a habit or task.")
    print("Let's build strong habits together—one lettuce leaf at a time!")
    print("READY TO START? LET'S GO!")
    print()

def main_menu():

    if os.path.exists("habits.json"):
        with open ("habits.json", "r") as file:
            habits = json.load(file)
            reminders = send_reminders(habits)
            if reminders:
                print("\n🔔 DAILY REMINDERS:")
            for r in reminders:
                print(r)
    


    while True:
        print("\n🐢 TOTO'S HABIT TRACKER MENU  🥬")
        print("1. Add a new habit") 
        print("2. View all habits")
        print("3. Daily check-in")
        print("4. View mood history")
        print("5. View streak history")
        print("6. View habit calendar")
        print("7. Edit or Delete Habit")
        print("8. Exit")
        print("9. Export habits to CSV")
        print("10. Export habits to HTML")
        choice = input("Please select an option (1 - 10): ")
        
        if choice == "1":
            add_habit()
        elif choice == "2":
            view_habits()
        elif choice == "3":
             daily_check_in()
        elif choice == "4":
            view_mood_history()  
        elif choice == "5":
            view_streak_history() 
        elif choice == "6":
            view_calendar() 
        elif choice == "7":
            edit_or_delete_habit()
        elif choice == "8":
            print("👋 Goodbye! Keep growing those habits,it's feeding Toto!")
        elif choice == "9":
            export_habits_to_csv()
        elif choice == "10":
            export_habits_to_html()
            
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 9.")
        
            

def add_habit():
    print("📝 Add a new habit!")
    name = input("Name of the habit: ")
    goal_per_day = int(input("How many times do you want to do this habit per day?"))
    goal_per_week = int(input("How many times per week do you want to do this habit?"))
    description = input("Description e.g. read 10 pages of a book:")
    importance = input(" How important is this habit to you? Low💛 / Medium🧡/ High❤️")

    #set up reminders
    reminders = {"default": [], "custom": {}}
    add_reminders = input("Do you want to add reminders? (yes/no):").lower()

    if add_reminders == "yes":
        use_default = input("Do you want to be reminded the same time everyday? (yes/no):").lower()
        if use_default == "yes":
           times = input("Enter times for reminders (e.g. 08:00, 12:00):")
           reminders["default"] = [t.strip() for t in times.split(",")]
        else:
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                day_times = input(f"Enter reminder time for {day} (e.g. 08:00):")
                if day_times.strip():
                    reminders["custom"][day] = [t.strip() for t in day_times.split(",")]

    new_habit = Habit(name,goal_per_day,goal_per_week, description, importance, reminders)

    # Load existing habits from JSON file
    habits = []
    if os.path.exists("habits.json"):
        with open("habits.json", "r") as file:
            habits = json.load(file)
    # Append the new habit to the list
    habits.append(new_habit.to_dict())
    # Save the updated list back to the JSON file
    with open("habits.json", "w") as file:
        json.dump(habits, file, indent=4)


    print("\n✅ Habit added successfully!")
    print(new_habit)

    



def view_habits():
    if not os.path.exists("habits.json"):
        print("😢 No habits found yet.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

        if not habits:
            print("😢 No habits saved yet.")
            return
        
        print("\n📋 Your Habits:")
        for idx, habit in enumerate(habits, start=1):
            print(f"\n{idx}. {habit['name']}")
            print(f"   Goal per day: {habit['goal_per_day']} times")
            print(f"   Goal per week: {habit['goal_per_week']} times")
            print(f"   Description: {habit['description']}")
            print(f"   Importance: {habit['importance']}")
            print(f"   Streak: {habit['streak']} days 🐾")

            #Weekly progress bar
            completions = habit.get("completions", [])
            current_week = datetime.now().isocalendar()[1]
            current_year = datetime.now().year

            # Count completions for the current week
            weekly_count = 0
            for date_str in completions:
                try:
                    date = datetime.fromisoformat(date_str)
                    if date.isocalendar()[1] == current_week and date.year == current_year:
                        weekly_count += 1
                except:
                    continue 
            
            bar = get_progress_bar(weekly_count, habit['goal_per_week'])
            print(f"  ➤ Weekly Progress: {bar}")
            
            
def daily_check_in():
    if not os.path.exists("habits.json"):
        print("😢 No habits to check in for.")
        return
    
    with open("habits.json", "r") as file:
        data = json.load(file)
    
    if not data:
        print("😢 Your habit list is empty.")
        return
    
    habits = [Habit.from_dict(h) for h in data]

    print("\n📅 Daily Check-in:")
    for idx, habit in enumerate(habits, start=1):
        print(f"\n{idx}. {habit.name}")
        
    choices = input("Which habit(s) did you complete today? (e.g., 1, 2, 3): ")
    indexes = [int(i) - 1 for i in choices.split() if i.isdigit()] 

    fed = 0
    for i in indexes:
        if 0 <= i < len(habits):
            if habits[i].mark_complete():
                print(f"✅ {habits[i].name} completed. Toto eats 🥬 !")
                fed += 1
            else:
                print(f"⚠️ Already completed today: {habits[i].name}")
      
    with open("habits.json", "w") as file:
        json.dump([h.to_dict() for h in habits], file, indent=4)

    mood = input("\n How are you feeling today? 😄😊😐😞😢: ") 
    today = datetime.date.today().isoformat()

    mood_log = []
    if os.path.exists("mood_log.json"):
        with open("mood_log.json", "r") as mood_file:
            mood_log = json.load(mood_file)

    mood_log.append({"date": today, "mood": mood})

    with open("mood_log.json", "w") as mood_file:
        json.dump(mood_log, indent = 4)
    

    print(f"🐢 Toto noted your mood: {mood}  💌")   

    if fed > 0:
        print(f"🐢 Toto is well fed ! You fed him {fed} lettuce{'s' if fed > 1 else ''} today!")
    else:
        print("🐢 Toto's stomach is rumbling. Why not try a task to feed him ? ")


def view_mood_history():
    if not os.path.exists("mood_log.json"):
        print("😢 No mood history found yet.")
        return
    
    
    with open("mood_log.json", "r") as mood_file:
        mood_log = json.load(mood_file)
    
    if not mood_log:
        print("😢 No mood history found.")
        return
    
    print("\n🧠 Mood History:")
    for entry in mood_log:
        print(f"Date: {entry['date']} | Mood: {entry['mood']}")




def edit_or_delete_habit():
    if not os.path.exists("habits.json"):
        print("😢 No habits to edit or delete.")
        return
    
    with open("habits.json", "r") as file:
        habits = json.load(file)

    if not habits:
        print("😢 Your habit list is empty.")
        return

    print("\n✏️ Select a habit to  Edit or Delete:")
    for idx, habit in enumerate(habits, start=1):
        print(f"{idx}. {habit['name']}")

    choice = input("Enter number of habit to edit/delete: ")
    if not choice.isdigit() or int(choice) not in range(1, len(habits) + 1):
        print("❌ Invalid selection.")
        return
    
    idx = int(choice) - 1 
    selected = habits[idx]

    print(f"\nSelected Habit: {selected['name']}")
    action =input("Do you want to edit (e) or delete (d) this habit? (e/d): ").lower()


    if action == 'e':
        print(" 🔄 Leave blank to keep the current value.")

        new_name = input(f"New name for [{selected['name']}]: ") or selected['name']
        new_day_goal = input(f"New goal per day [{selected['goal_per_day']}]: ") or selected['goal_per_day']
        new_week_goal = input(f"New goal per week [{selected['goal_per_week']}]: ") or selected['goal_per_week']
        new_description = input(f"New description [{selected['description']}]: ") or selected['description']
        new_importance = input(f"New importance [{selected['importance']}]: ") or selected['importance']
        
        selected['name'] = new_name
        selected['goal_per_day'] = int(new_day_goal)
        selected['goal_per_week'] = int(new_week_goal)
        selected['description'] = new_description
        selected['importance'] = new_importance

        habits[idx] = selected 
        print(f"✏️ Habit successfully updated!")

    elif action == 'd':
        habits.remove(selected)
        print(f"🗑️ Habit {selected['name']} deleted!")
    else:
        print("❌ Invalid action.")

    with open("habits.json", "w") as file:
        json.dump(habits, file, indent=4)
        
if __name__ == "__main__":
    welcome_screen()
    main_menu()