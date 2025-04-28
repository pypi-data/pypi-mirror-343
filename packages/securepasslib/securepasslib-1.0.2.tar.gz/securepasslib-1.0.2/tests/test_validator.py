from securepasslib.policy import PasswordPolicy
from securepasslib.validator import Validator

def test_valid_password():
    policy = PasswordPolicy()  # Use default policy
    validator = Validator(policy)
    pwd = "Aa1!aaaa"
    errors = validator.validate(pwd)
    assert errors == []  # No errors means the password is valid

def test_invalid_password():
    policy = PasswordPolicy()  # Use default policy
    validator = Validator(policy)
    pwd = "1234"
    errors = validator.validate(pwd)
    assert len(errors) > 0
    assert any("at least" in e for e in errors)  # Check that it detects missing requirements


def test_custom_policy_valid_password():
    # Custom policy: minimum 10 chars, 2 uppercase, 2 digits, 1 special
    policy = PasswordPolicy(
        min_length=10,
        min_uppercase=2,
        min_digits=2,
        min_special=1
    )
    validator = Validator(policy)

    pwd = "AAstrong11!"
    errors = validator.validate(pwd)

    assert errors == []  # Should pass with no errors

def test_custom_policy_invalid_password():
    # Same custom policy as above
    policy = PasswordPolicy(
        min_length=10,
        min_uppercase=2,
        min_digits=2,
        min_special=1
    )
    validator = Validator(policy)

    pwd = "Astrong1"  # Too short, only 1 uppercase, 1 digit, 0 special
    errors = validator.validate(pwd)

    assert len(errors) >= 1
    assert "at least" in errors[0] or "must contain" in errors[0]  # Error message related to missing rule


def test_strength_scoring():
    validator = Validator()

    assert validator.strength_score("abc") == (1, "Very Weak")
    assert validator.strength_score("abcdefg1") == (3, "Weak")
    assert validator.strength_score("Abcdef12") == (4, "Medium")
    assert validator.strength_score("tcdAbcd12!") == (5, "Strong")
    assert validator.strength_score("1234Abcd1234!@") == (6, "Very Strong")
    
    
def test_entropy_calculation():
    validator = Validator()
    entropy = validator.calculate_entropy("Password123!")
    assert entropy > 0

def test_suggest_improvements():
    validator = Validator()
    suggestions = validator.suggest_improvements("abc")
    assert len(suggestions) > 0

def test_get_password_report_complete():
    validator = Validator()
    report = validator.get_password_report("password123")
    assert "entropy_bits" in report
    assert "suggestions" in report