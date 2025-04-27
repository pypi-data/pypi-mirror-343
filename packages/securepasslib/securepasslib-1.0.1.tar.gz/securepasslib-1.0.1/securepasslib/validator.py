
import re
from .policy import PasswordPolicy  # 👈 Import from the new file
from .constants.patterns import UPPERCASE_PATTERN, LOWERCASE_PATTERN, DIGIT_PATTERN, SPECIAL_PATTERN
from .constants.messages import (
    TOO_SHORT,
    NOT_ENOUGH_UPPERCASE,
    NOT_ENOUGH_LOWERCASE,
    NOT_ENOUGH_DIGITS,
    NOT_ENOUGH_SPECIAL,
)

import math

class Validator:
    def __init__(self, policy: PasswordPolicy = PasswordPolicy()):
        self.policy = policy

    def validate(self, password: str) -> list[str]:
        errors = []
        
        if len(password) < self.policy.min_length:
            errors.append(TOO_SHORT.format(min_length=self.policy.min_length))

        if len(re.findall(UPPERCASE_PATTERN, password)) < self.policy.min_uppercase:
            errors.append(NOT_ENOUGH_UPPERCASE.format(min_uppercase=self.policy.min_uppercase))

        if len(re.findall(LOWERCASE_PATTERN, password)) < self.policy.min_lowercase:
            errors.append(NOT_ENOUGH_LOWERCASE.format(min_lowercase=self.policy.min_lowercase))

        if len(re.findall(DIGIT_PATTERN, password)) < self.policy.min_digits:
            errors.append(NOT_ENOUGH_DIGITS.format(min_digits=self.policy.min_digits))

        if len(re.findall(SPECIAL_PATTERN, password)) < self.policy.min_special:
            errors.append(NOT_ENOUGH_SPECIAL.format(min_special=self.policy.min_special))

        return errors
    def is_strong(self, password: str, min_length: int = 8) -> bool:
        return (
            len(password) >= min_length and
            re.search(UPPERCASE_PATTERN, password) and
            re.search(LOWERCASE_PATTERN, password) and
            re.search(DIGIT_PATTERN, password) and
            re.search(SPECIAL_PATTERN, password)
        )
    
    def strength_score(self, password: str) -> tuple[int, str]:
        score = 0

        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1  # bonus for longer passwords
        if re.search(UPPERCASE_PATTERN, password):
            score += 1
        if re.search(LOWERCASE_PATTERN, password):
            score += 1
        if re.search(DIGIT_PATTERN, password):
            score += 1
        if re.search(SPECIAL_PATTERN, password):
            score += 1

        if score <= 2:
            strength = "Very Weak"
        elif score == 3:
            strength = "Weak"
        elif score == 4:
            strength = "Medium"
        elif score == 5:
            strength = "Strong"
        else:
            strength = "Very Strong"

        return score, strength

    def get_password_report(self, password: str) -> dict:
        errors = self.validate(password)
        score, strength = self.strength_score(password)

        return {
            "errors": errors,
            "strength_score": score,
            "strength_text": strength
        }

    def calculate_entropy(self, password: str) -> float:
        """Calculate entropy of a password in bits."""
        pool_size = 0
        if re.search(LOWERCASE_PATTERN, password):
            pool_size += 26
        if re.search(UPPERCASE_PATTERN, password):
            pool_size += 26
        if re.search(DIGIT_PATTERN, password):
            pool_size += 10
        if re.search(SPECIAL_PATTERN, password):
            pool_size += 32  # Estimate symbols

        if pool_size == 0:
            return 0.0

        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)
    
    def suggest_improvements(self, password: str) -> list[str]:
        """Suggest improvements for a weak password."""
        suggestions = []

        if len(password) < 12:
            suggestions.append("Increase password length to at least 12 characters.")
        if not re.search(UPPERCASE_PATTERN, password):
            suggestions.append("Add at least one uppercase letter.")
        if not re.search(LOWERCASE_PATTERN, password):
            suggestions.append("Add at least one lowercase letter.")
        if not re.search(DIGIT_PATTERN, password):
            suggestions.append("Add at least one number.")
        if not re.search(SPECIAL_PATTERN, password):
            suggestions.append("Add at least one special character (!@#$...)")

        return suggestions
    
    def get_password_report(self, password: str) -> dict:
        errors = self.validate(password)
        score, strength = self.strength_score(password)
        entropy = self.calculate_entropy(password)
        suggestions = self.suggest_improvements(password)

        return {
            "errors": errors,
            "strength_score": score,
            "strength_text": strength,
            "entropy_bits": entropy,
            "suggestions": suggestions
        }
