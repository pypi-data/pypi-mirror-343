from dataclasses import dataclass
from securepasslib.constants.settings import DEFAULT_MIN_LENGTH , DEFAULT_MIN_UPPERCASE, DEFAULT_MIN_LOWERCASE , DEFAULT_MIN_DIGITS , DEFAULT_MIN_SPECIAL


@dataclass
class PasswordPolicy:
    min_length: int = DEFAULT_MIN_LENGTH
    min_uppercase: int = DEFAULT_MIN_UPPERCASE
    min_lowercase: int = DEFAULT_MIN_LOWERCASE
    min_digits: int = DEFAULT_MIN_DIGITS
    min_special: int = DEFAULT_MIN_SPECIAL