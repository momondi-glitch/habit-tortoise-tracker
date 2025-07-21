def get_progress_bar(current, goal, bar_length=20):
    filled_length = int(bar_length * current // goal) if goal > 0 else 0
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    return f"[{bar}] {current}/{goal}"
