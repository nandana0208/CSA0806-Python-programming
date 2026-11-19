from attendance_utils import percentage, three_day_absences
if __name__ == "__main__":
    print(f"Attendance: {percentage(18,2):.1f}%")
    print("Three consecutive absences:", three_day_absences(["P","A","A","A"]))
