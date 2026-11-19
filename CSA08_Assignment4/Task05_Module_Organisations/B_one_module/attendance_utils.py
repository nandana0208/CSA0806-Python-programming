def percentage(present, absent):
    total = present + absent
    return present / total * 100 if total else 0
def three_day_absences(statuses):
    return any(statuses[i:i+3] == ["A", "A", "A"] for i in range(len(statuses)-2))
