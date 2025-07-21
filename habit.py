import datetime
class Habit:
    def __init__(self, name, goal_per_day, goal_per_week, description, importance, reminders=None):
        self.name = name
        self.goal_per_day = goal_per_day
        self.goal_per_week = goal_per_week
        self.description = description
        self.importance = importance
        self.streak = 0
        self.completions =[]
        self.milestones_hit = []
        self.reminders = reminders or {"default": [], "custom": {}}
    
    def mark_complete(self):
        today = datetime.date.today().isoformat()
        if today not in self.completions:
            self.completions.append(today)
            self.streak += 1
            milestones = [3,7,14,21,30]
            celebrated = []

            for m in milestones:
                if self.streak == m and m not in self.milestones_hit:
                    print(f"\n🎉🎉 STREAK MILESTONE UNLOCKED! {self.name} - {m} days in a row! Toto is PROUD 🐢🥬")
                    self.milestones_hit.append(m)
                    celebrated.append(m)
            return True
        return False
    
    def to_dict(self) :
        return {
            "name": self.name,
            "goal_per_day": self.goal_per_day,
            "goal_per_week": self.goal_per_week,
            "description": self.description,
            "importance": self.importance,
            "streak": self.streak,
            "completions": self.completions,
            "milestones_hit": self.milestones_hit,
            "reminders": self.reminders
        }
    @classmethod
    def from_dict(cls, data):
        habit = cls(
            data["name"],
            data["goal_per_day"],
            data["goal_per_week"],
            data["description"],
            data["importance"]
        )
        habit.streak = data["streak"]
        habit.completions = data["completiions"]
        habit.milestones_hit = data.get("milestones_hit", [])
        habit.reminders = data.get("reminders", {"default": [], "custom": {}})
        return habit 
     

    def __str__(self):
        return f"Habit: {self.name} | Goal: {self.goal_per_day}x/day | Goal: {self.goal_per_week}x/week | Importance: {self.importance}"
    
