def duration_formatter(duration):
    hours = duration // 3600
    minutes = format_to_timer((duration % 3600) // 60)
    seconds = format_to_timer(duration % 60)
    if hours > 0:
        return f"{format_to_timer(hours)}:{minutes}:{seconds}"
    else:
        return f"{minutes}:{seconds}"
    
def format_to_timer(time):
    return int(time) if time >= 10 else f"0{int(time)}"
    
