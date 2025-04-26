import re

def is_strong(password: str, min_length: int = 8) -> bool:
    return (
        len(password) >= min_length and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )

def validate(password: str, min_length=8):
    errors = []
    if len(password) < min_length:
        errors.append("Password is too short.")
    if not re.search(r"[A-Z]", password):
        errors.append("Must include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Must include at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Must include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Must include at least one special character.")
    return errors
