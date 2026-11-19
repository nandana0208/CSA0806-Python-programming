class InvalidRegistration(Exception):
    """A registration row is damaged or invalid."""

def valid_email(email):
    email = email.strip()
    if not email or " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local and domain and "." in domain and
                not domain.startswith(".") and not domain.endswith("."))

def parse_registration(line):
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(parts)}")
    reg, name, department, email, event_text = parts
    if not reg or not name or not department:
        raise InvalidRegistration("register, name and department are required")
    if not valid_email(email):
        raise InvalidRegistration(f"invalid email {email!r}")
    events = {event.strip() for event in event_text.split(";") if event.strip()}
    if not events:
        raise InvalidRegistration("at least one event is required")
    return {"register": reg, "name": name, "department": department,
            "email": email.lower(), "events": events}
