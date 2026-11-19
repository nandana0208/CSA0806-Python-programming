from stats import percentage, three_day_absences
from report import show
if __name__ == "__main__":
    show(percentage(18,2), three_day_absences(["P","A","A","A"]))
