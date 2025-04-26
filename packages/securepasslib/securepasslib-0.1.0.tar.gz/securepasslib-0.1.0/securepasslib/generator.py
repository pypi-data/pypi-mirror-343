import random
import string

def generate_password(length=12, use_upper=True, use_digits=True, use_special=True):
    if length < 6:
        raise ValueError("Password length must be at least 6 characters.")
    
    chars = list(string.ascii_lowercase)
    if use_upper:
        chars += list(string.ascii_uppercase)
    if use_digits:
        chars += list(string.digits)
    if use_special:
        chars += list("!@#$%^&*()_+=[]{}|;:,.<>?")

    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))
