import random
import string
from .constants.templates import TEMPLATES

class PasswordGenerator:
    def __init__(self):
        # Define character pools
        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special = "!@#$%^&*()_+=[]{}|;:,.<>?/"

    def generate_random_password(self, length=12, use_upper=True, use_digits=True, use_special=True):
        if length < 6:
            raise ValueError("Password length must be at least 6 characters.")
        
        chars = list(string.ascii_lowercase)
        if use_upper:
            chars += list(string.ascii_uppercase)
        if use_digits:
            chars += list(string.digits)
        if use_special:
            chars += list(self.special)

        return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

    def generate_by_template(self, template_name: str= None, custom_template: str = None) -> str:
        if custom_template:
            template = custom_template
        elif template_name:
            template = TEMPLATES.get(template_name)
            if not template:
                raise ValueError(f"Template '{template_name}' not found.")
        else:
            raise ValueError("Must provide either a template_name or custom_template.")

        result = []
        for char in template:
            if char == 'L':
                result.append(random.choice(string.ascii_letters))
            elif char == 'D':
                result.append(random.choice(string.digits))
            elif char == 'S':
                result.append(random.choice(self.special))
            elif char == 'W':
                # Generate a random short word
                word = self._generate_word()
                result.append(word)
            elif char == '-':
                result.append('-')
            else:
                result.append(char)  # keep literal characters

        return ''.join(result)

    def _generate_word(self, length=5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
