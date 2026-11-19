def read_statuses(lines):
    return [line.strip().split(",")[-1] for line in lines if line.strip()]
