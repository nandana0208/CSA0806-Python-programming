def percentage(present, absent):
    total = present + absent
    return present / total * 100 if total else 0
def three_day_absences(statuses):
    return any(statuses[i:i+3] == ["A", "A", "A"] for i in range(len(statuses)-2))
if __name__ == "__main__":
    print(f"Attendance: {percentage(18,2):.1f}%")
    print("Three consecutive absences:", three_day_absences(["P","A","A","A"]))
